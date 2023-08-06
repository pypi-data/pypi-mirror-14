from exceptions import *

import os
import sys
import json

class _Attr_:
    '''
    This is an empty class used to hold functions and attributes passed to the
    TestExecutor.
    '''
    pass

class _TestDefParser_:
    '''
    This class is used to parse test step definition files in the given
    directory.
    '''
    def __init__(self, defpath):
        self.defpath = defpath

    def parse_file(self, filename):
        f = None
        try:
            path = "%s/%s" %(self.defpath, filename)
            f = open(path, "r")
            testdef = json.loads(f.read())
                
        except IOError as e:
            msg = "Unable to open file"
            try:
                msg = msg + ", " + str(path)
                msg = msg + ": " + str(e)
            except (TypeError, ValueError):
                pass
            raise SpyteError(msg)
                
        except (TypeError, ValueError) as e:
            msg = "JSON decoding failed"
            try:
                msg = msg + " in " + str(path)
                msg = msg + ": " + str(e)
            except (TypeError, ValueError):
                pass
            raise SpyteError(msg)

        if f:
            f.close()

        self._verify_testdef_fmt_(testdef)

        return testdef

    def _verify_testdef_fmt_(self, testdef):
        try:
            assert isinstance(testdef, dict)
        except AssertionError as e:
            raise SpyteError(
                "Body of %s is not a JSON object: %s"
                %(str(self.defpath), str(e)))

        for stepname, stepdef in testdef.iteritems():
            if not isinstance(stepname, unicode):
                msg = "Step name in %s is not a string" %(self.defpath)
                try:
                    msg = msg + ', "%s"' %(str(stepname))
                except (TypeError, ValueError):
                    pass
                raise SpyteError(msg)
        
            if not isinstance(stepdef, dict):
                raise SpyteError(
                    "%s in %s is not a JSON object" %(stepname, self.defpath))
                
            self._verify_stepdef_fmt_(stepdef, stepname)
                
    def _verify_stepdef_fmt_(self, stepdef, stepname):
        for key in stepdef:
            if not key in ["desc", "params", "substep"]:
                msg = ('%s in %s is contains invalid key'
                       %(stepname, self.defpath))
                try:
                    msg = msg + ', "%s"' %(str(key))
                except (TypeError, ValueError):
                    pass
                raise SpyteError(msg)
                
        for key, valtype, typename in [("desc", unicode, "string"),
                                       ("params", dict, "JSON object"),
                                       ("substep", dict, "JSON object")]:
            if not key in stepdef:
                raise SpyteError(
                    '%s in %s is missing "%s"'
                    %(stepname, self.defpath, key))

            if not isinstance(stepdef[key], valtype):
                raise SpyteError(
                    '%s in step %s in %s is not a %s'
                    %(key, stepname, self.defpath, typename))
            
        params = stepdef["params"]
        substepdef = stepdef["substep"]
        self._verify_substepdef_fmt_(substepdef, stepname, params)

    def _verify_substepdef_fmt_(self, substepdef, stepname, params):
        msg = 'The substep for step %s in %s' %(stepname, self.defpath)

        if (substepdef["type"] == "and" or
            substepdef["type"] == "or" or
            substepdef["type"] == "all"):
            keys = {
                "type":            unicode,
                "set":             list}

        elif substepdef["type"] == "func":
            keys = {
                "type":            unicode,
                "path":            unicode,
                "args":            list,
                "kwargs":          dict,
                "expected_result": None}

        elif substepdef["type"] == "step":
            keys = {
                "type":            unicode,
                "path":            unicode,
                "params":          dict}

        else:
            msg = msg + ' contains an unknown type'
            try:
                msg = msg + ": " + str(substepdef["type"])
            except (ValueError, TypeError):
                pass
            raise SpyteError(msg)

        for key, type_ in keys.iteritems():
            if not key in substepdef:
                raise SpyteError(
                    msg + ' is missing required key "%s"' %(key))

            if type_ and not isinstance(substepdef[key], type_):
                if type(type_) == unicode:
                    type_str = "string"
                elif type(type_) == list:
                    type_str = "JSON array"
                elif type(type_) == dict:
                    type_str = "JSON object"
                    
                raise SpyteError(
                    msg + ' contains %s that is not a %s' %(key, type_str))
                

        for key in substepdef:
            if not key in keys:
                raise SpyteError(
                    msg + ' contains an unknown key "%s"' %(key))

        if (substepdef["type"] == "and" or
            substepdef["type"] == "or" or
            substepdef["type"] == "all"):

            for next_substepdef in substepdef["set"]:
                self._verify_substepdef_fmt_(next_substepdef, stepname, params)

        elif substepdef["type"] == "func":
            for paramdef in substepdef["args"]:
                self._verify_paramdef_fmt_(paramdef, stepname, params)

            for paramname, paramdef in substepdef["kwargs"].iteritems():
                self._verify_paramdef_fmt_(
                    paramdef, stepname, params, paramname)

        elif substepdef["type"] == "step":
            for paramname, paramdef in substepdef["params"].iteritems():
                self._verify_paramdef_fmt_(
                    paramdef, stepname, params, paramname)

    def _verify_paramdef_fmt_(self, paramdef, stepname, params,
                              paramname = None):

        msg = ('The substep from step %s in %s' %(stepname, self.defpath))

        if paramname and not isinstance(paramname, unicode):
            msg = msg + ' contains a param key that is not a string'
            try:
                msg = msg + ": " + str(paramname)
            except (TypeError, ValueError):
                pass
            raise SpyteError(msg)

        if not isinstance(paramdef, dict):
            msg = msg + ' contains a param that is not a JSON object'
            if paramname:
                msg = msg + ': ' + paramname
            raise SpyteError(msg)

        if not "type" in paramdef:
            msg = msg + ' contains a param that does not have a "type" key'
            if paramname:
                msg = msg + ': ' + paramname
            raise SpyteError(msg)
            
        if not paramdef["type"] in ["byval", "byref"]:
            msg = msg + ' contains a param without type "byref" or "byval"'
            if paramname:
                msg = msg + ': ' + paramname
            raise SpyteError(msg)
            
        keys = []
        if paramdef["type"] == "byref":
            if not "ref" in paramdef or not paramdef["ref"] in params:
                msg = msg + ' contains a "byref" param without valid "ref"'
                if paramname:
                    msg = msg + ': ' + paramname
                raise SpyteError(msg)

            keys = ["type", "ref"]
            
        elif paramdef["type"] == "byval":
            if not "val" in paramdef:
                msg = msg + ' contains a "byval" param without valid "val"'
                if paramname:
                    msg = msg + ': ' + paramname
                raise SpyteError(msg)

            keys = ["type", "val"]

        else:
            msg = msg + ' contains a param without type "byref" or "byval"'
            if paramname:
                msg = msg + ': ' + paramname
            raise SpyteError(msg)
            
        for key in paramdef:
            if not key in keys:
                msg = msg + ' contains a param with unknown key'
                try:
                    msg = msg + ", " + str(key)
                except (TypeError, ValueError):
                    pass
                if paramname:
                    msg = msg + ': ' + paramname
                raise SpyteError(msg)

    def verify_stepdef_fmt(self, stepdef):
        stepname = "unknown"
        try:
            stepname = self.defpath.split(".")[-1]
        except (TypeError, ValueError, LookupError) as e:
            msg = "Unable to parse stepname from path"
            try:
                msg = msg + ": " + str(self.defpath)
            except (TypeError, ValueError):
                pass
            raise SpyteError(msg)

        self._verify_stepdef_fmt_(stepdef, stepname)

class TestExecutor:
    def __init__(self,
                 defpath,
                 _prestep_cb_ = None,
                 _poststep_cb_ = None,
                 _prefunc_cb_ = None,
                 _postfunc_cb_ = None,
                 **kwargs):
        '''
        Initializes test executor and starts the logger.

        @param defpath -         Path to directory containing *.json test step
                                 definition files.
        @param _prestep_cb_ -    (Optional) Callback that is called immediately
                                 prior to running a test step. See prototype
                                 self.prestep_cb().
        @param _poststep_cb_ -   (Optional) Callback that is called immediately
                                 after a test step finished running. See
                                 prototype self.poststep_cb().
        @param _prefunc_cb_ -    (Optional) Callback that is called immediately
                                 prior to calling a function referenced in a
                                 test step. See prototype self.prestep_cb().
        @param _postfunc_cb_ -   (Optional) Callback that is called immediately
                                 after function referenced within a test step
                                 returns. See prototype self.poststep_cb().
        @param **kwargs -        Pass any number of key value pairs after
                                 required and optional parameters to initialize
                                 the test executor. Each item then becomes
                                 self.<key> = <value>.
        '''
        self._defpath_ = defpath

        if _prestep_cb_:
            self.prestep_cb = _prestep_cb_

        if _poststep_cb_:
            self.poststep_cb = _poststep_cb_

        if _prefunc_cb_:
            self.prefunc_cb = _prefunc_cb_

        if _postfunc_cb_:
            self.postfunc_cb = _postfunc_cb_

        if not os.path.exists(self._defpath_):
            msg = "Test def directory does not exist"
            try:
                msg = msg + ": " + str(self._defpath_)
            except (TypeError, ValueError) as e:
                pass
            raise SpyteError(msg)

        self.attr = _Attr_()
        self.defs = {}

        for key, attr in kwargs.iteritems():
            setattr(self.attr, key, attr)

        self._parser_ = _TestDefParser_(self._defpath_)
        for filename in os.listdir(self._defpath_):
            if filename.endswith(".json"):
                testdef = self._parser_.parse_file(filename)
                self.defs[filename.replace(".json", "")] = testdef

    def _is_subset_(self, set1, set2):
        if type(set1) != type(set2):
            return False

        elif isinstance(set1, dict):
            for key in set1:
                if not key in set2:
                    return False
                if not self._is_subset_(set1[key], set2[key]):
                    return False

        elif isinstance(set1, list):
            if len(set1) > len(set2):
                return False
            for i in range(0,len(set1)):
                if not self._is_subset_(set1[i], set2[i]):
                    return False

        else:
            if set1 != set2:
                return False

        return True

    def _resolve_params_(self, paramslist, parent_params):
        if isinstance(paramslist, list):
            resolved_params = []
            for param in paramslist:
                if param["type"] == "byval":
                    resolved_params.append(param["val"])
                elif param["type"] == "byref":
                    resolved_params.append(parent_params[param["ref"]])

        elif isinstance(paramslist, dict):
            resolved_params = {}
            for key, param in paramslist.iteritems():
                if param["type"] == "byval":
                    resolved_params[key] = param["val"]
                elif param["type"] == "byref":
                    resolved_params[key] = parent_params[param["ref"]]

        return resolved_params

    def _exec_substeps_(self, _substepdef_, _paths_, **kwargs):
        success = True
        errors = []
        results = []
        paths = _paths_[:]
        
        if _substepdef_["type"] == "func":
            path = _substepdef_["path"]
            args = self._resolve_params_(_substepdef_["args"], kwargs)
            kwargs_ = self._resolve_params_(_substepdef_["kwargs"], kwargs)
            expected_result = _substepdef_["expected_result"]
            func_result = None
            func_errors = []
            func_success = True

            paths.append(path)

            try:
                self.prefunc_cb(paths = paths,
                                args = args,
                                kwargs = kwargs_)
            except Exception as e:
                pass

            try:
                func = self.resolve_path(path)
                func_result = func(*args, **kwargs_)
                if not self._is_subset_(expected_result, func_result):
                    msg = "Unexpected result"
                    try:
                        msg = msg + " for %s" %(str(path))
                        msg = msg + ", expected `%s`" %(str(expected_result))
                        msg = msg + ", got `%s`" %(str(func_result))
                    except (ValueError, TypeError):
                        pass
                    raise SpyteError(msg)

            except Exception as error:
                success = False
                func_success = False
                func_errors.append({
                    "type":type(error).__name__,
                    "msg":str(error)
                })

            result = {
                "type": "func",
                "path": path,
                "args": args,
                "kwargs": kwargs_,
                "expected_result": expected_result,
                "result": func_result,
                "success": func_success,
                "errors": func_errors,
            }

            try:
                self.postfunc_cb(paths = paths, result = result)
            except Exception as e:
                pass

            results.append(result)

        elif _substepdef_["type"] == "step":
            try:
                path = _substepdef_["path"]
                params = self._resolve_params_(_substepdef_["params"], kwargs)
                stepdef = self.resolve_path(path)
                paths.append(path)
                result = self._exec_step_(stepdef, paths, **params)
                results.append(result)
                success = result["success"]
            except Exception as error:
                errors.append({
                    "type":type(error).__name__,
                    "msg":str(error)
                })
                success = False
                
        elif _substepdef_["type"] == "all":
            for next_substepdef in _substepdef_["set"]:
                step_success, step_errors, step_results = self._exec_substeps_(
                    next_substepdef, paths, **kwargs)
                errors = errors + step_errors
                results = results + step_results
                if not step_success:
                    success = False

        elif _substepdef_["type"] == "and":
            for next_substepdef in _substepdef_["set"]:
                step_success, step_errors, step_results = self._exec_substeps_(
                    next_substepdef, paths, **kwargs)
                errors = errors + step_errors
                results = results + step_results
                if not step_success:
                    success = False
                    break
                
        elif _substepdef_["type"] == "or":
            success = False
            for next_substepdef in _substepdef_["set"]:
                step_success, step_errors, step_results = self._exec_substeps_(
                    next_substepdef, paths, **kwargs)
                errors = errors + step_errors
                results = results + step_results
                if step_success:
                    success = True
                    break

        else:
            success == False
            msg = "Test step was incorrectly defined"
            try:
                msg = msg + ": `%s`" %(str(_substepdef_))
            except (TypeError, ValueError):
                pass
            error = SpytError(msg)
            errors.append({
                "type":type(error).__name__,
                "msg":str(error)
            })

        return success, errors, results

    def _exec_step_(self, _stepdef_, _paths_, **kwargs):
        paths = _paths_[:]

        params = {}

        try:
            self.prestep_cb(stepdef = _stepdef_,
                            paths = paths,
                            params = kwargs)
        except Exception as e:
            pass

        for key in _stepdef_["params"]:
            if key in kwargs:
                params[key] = kwargs[key]

        ret = {
            "type": "step",
            "path": paths[-1],
            "desc": _stepdef_["desc"],
            "params": params,
        }
        
        ret["success"], ret["errors"], ret["substeps"] = self._exec_substeps_(
            _stepdef_["substep"], paths, **params)
        
        try:
            self.poststep_cb(stepdef = _stepdef_,
                             paths = paths,
                             params = kwargs,
                             result = ret)
        except Exception as e:
            pass

        return ret

    def prestep_cb(self,
                   stepdef = None,
                   paths = None,
                   params = None):
        '''
        Optional callback (set by __init__()) called just prior to executing
        a test step.

        @param stepdef -  The JSON dictionary which defines the test step that
                          is about to be run-- matches the JSON object provided
                          in the *.json test step definition files.
        @param paths -    A list of the paths of each step followed to get to
                          the current step. The path to this step is at
                          paths[-1].
        @param params -   A dictionary containing the key-value pairs of each
                          parameter being passed to this test step.
        '''
        pass

    def poststep_cb(self,
                    stepdef = None,
                    paths = None,
                    result = None):
        '''
        Optional callback (set by __init__()) called just after executing a
        test step.

        @param stepdef -  The JSON dictionary which defines the test step that
                          is about to be run-- matches the JSON object provided
                          in the *.json test step definition files.
        @param paths -    A list of the paths of each step followed to get to
                          the current step. The path to this step is at
                          paths[-1].
        @param result -   The result dictionary which would be returned by
                          "run()" function if it had been called with the path
                          of this step.
        '''
        pass

    def prefunc_cb(self,
                   paths = None,
                   args = None,
                   kwargs = None,
                   expected_result = None):
        '''
        Optional callback (set by __init__()) called right before executing
        a function referred to in a test step.

        @param paths -           A list of the paths of each step followed to
                                 get to the current step. The path to this step
                                 is at paths[-1].
        @param args -            A list containing the ordered values of any
                                 unnamed function parameters being passed to
                                 this function.
        @param kwargs -          A dictionary containing the key-value pairs of
                                 each named parameter being passed to this
                                 function.
        @param expected_result - The result (or a subset of the result if it's
                                 a list or dict) that the function is expected
                                 to return.
        '''
        pass

    def postfunc_cb(self,
                    paths = None,
                    result = None):
        '''
        Optional callback (set by __init__()) called right after executing
        a function referred to in a test step.

        @param paths -  A list of the paths of each step followed to get to the
                        current step. The path to this step is at paths[-1].
        @param result - The result dictionary which would be returned in the
                        "substep" field of the response to the "run()" function
                        if it had been called with the path of this function's
                        parent step.
        '''
        pass

    def resolve_path(self, path):
        '''
        Resolves a path down to the function or test step definition dictionary
        to which it points.

        @param path - A dot-separated path to a function in self.attr or a test
                      step definition dictionary in self.defs-- as such, the
                      path must begin with "attr." or "defs."

        @throws SpyteError if the path cannot be resolved to a function or test
                           step definition.
        '''
        attr = self
        try:
            path_attrs = path.split(".")
            assert path_attrs[0] in ["attr", "defs"]
        except (TypeError, AssertionError):
            msg = "Path does not begin with defs or attr"
            try:
                msg = msg + ": " + str(path)
            except (ValueError, TypeError) as e:
                pass
            raise SpyteError(msg)

        for path_attr in path_attrs:
            if hasattr(attr, path_attr):
                attr = getattr(attr, path_attr)
            elif isinstance(attr, dict) and path_attr in attr:
                attr = attr[path_attr]
            else:
                msg = "Failed to resolve path"
                try:
                    msg = msg + ": " + str(path)
                except (ValueError, TypeError) as e:
                    pass
                raise SpyteError(msg)

        return attr

    def run(self, path, **kwargs):
        '''
        Executes the function or test step defined in a *.json test def file
        within self.defpath. When self is initialized all def files become
        keys in the self.defs dictionary with their values being the parsed
        JSON object in the body of the test def file.

        @param path - The path to a test step in a test def file, defined using
                      "defs", the name of the file (without the file
                      extension), and the name of one of the steps defined
                      therein as follows: "defs.<filename>.<stepname>"

        @param kwargs - An unbound number of key-value pairs representing the
                        parameters that are to be passed to this test step.

        @return This function returns a JSON-like dictionary containing the
                following information:

                {
                  "type": "step",
                  "path": <string_with_path_to_step_definition>,
                  "desc": <string_with_description_from_definition>,
                  "params": <dict_with_key_value_pairs_passed_to_step>,
                  "success": <True/False>,
                  "errors": [
                    {
                      "type": <name_of_exception_type>,
                      "msg": <descriptive_exception_msg>
                    },
                    ...
                  ]
                  "substeps": <list_of_substep_results>
                }
                
                Where <list_of_substep_results> is an ordered list containing
                the same result dictionary for each substep executed as part
                of this step. All test steps should eventually resolve to a
                function call. The result dictionary of function calls differs
                as follows:
                
                {
                  "type": "func",
                  "path": <string_with_path_to_step_definition>,
                  "args": <list_with_unnamed_parameters_passed_to_func>,
                  "kwargs": <dict_with_named_parameters_passed_to_func>,
                  "expected_result": <expected_result_of_function>,
                  "result": <actual_result_of_function>,
                  "success": <True/False>,
                  "errors": [
                    {
                      "type": <name_of_exception_type>,
                      "msg": <descriptive_exception_msg>
                    },
                    ...
                  ]
                }
        '''
        return self._exec_step_(self.resolve_path(path), [path], **kwargs)

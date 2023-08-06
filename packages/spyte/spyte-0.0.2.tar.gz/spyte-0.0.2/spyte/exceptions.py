class SpyteError(Exception):
    dflt_msg = "Spyte Exception"
    def __init__(self, msg = None):
        new_msg = self.dflt_msg
        if msg:
            new_msg = "%s: %s" %(new_msg, msg)
        Exception.__init__(self, new_msg)

class LoggerInitError(SpyteError):
    dflt_msg = "The logger has not been started"

class _FailedTestStep_(Exception):
    dflt_msg = "Failed Test Step"
    def __init__(self, msg = None):
        new_msg = self.dflt_msg
        if msg:
            new_msg = "%s: %s" %(new_msg, msg)
        Exception.__init__(self, new_msg)
 

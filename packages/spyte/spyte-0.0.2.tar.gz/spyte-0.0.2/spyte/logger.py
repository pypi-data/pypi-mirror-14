import time

from spyte.threads import QueueThread
from spyte.exceptions import LoggerInitError
from spyte.ui import cli

global _log_
global _request_

_log_ = None
_request_ = None

class _ENTRY_TYPE_:
    INFO =    0
    SUCCESS = 1
    BOLD =    2
    WARN =    3
    ERROR =   4

_PRINT_COLOR_ = {
    _ENTRY_TYPE_.INFO:    "\x1b[37m%s\x1b[0m",   # White
    _ENTRY_TYPE_.SUCCESS: "\x1b[1;32m%s\x1b[0m", # Green
    _ENTRY_TYPE_.BOLD:    "\x1b[1;34m%s\x1b[0m", # Blue
    _ENTRY_TYPE_.WARN:    "\x1b[1;33m%s\x1b[0m", # Yellow
    _ENTRY_TYPE_.ERROR:   "\x1b[1;31m%s\x1b[0m", # Red
}

_LOG_ABRV_ = {
    _ENTRY_TYPE_.INFO:    "   ",
    _ENTRY_TYPE_.SUCCESS: "+++",
    _ENTRY_TYPE_.BOLD:    ">>>",
    _ENTRY_TYPE_.WARN:    "WRN",
    _ENTRY_TYPE_.ERROR:   "ERR",
}

class _LogEntry_:
    def __init__(self, entrytype, data, doprint = True):
        self.timestamp = time.time()
        self.entrytype = entrytype
        self.data = data
        self.doprint = doprint

class _LogWorker_(QueueThread):
    def __init__(self,
                 filename = None,
                 initFunc = None,
                 cleanupFunc = None,
                 logFmtFunc = None,
                 printFmtFunc = None,
                 finishBeforeStop = True):

        QueueThread.__init__(self, finishBeforeStop)
        self.logfile = None
        self.unloggedLines = []
        self.initFunc = initFunc
        self.cleanupFunc = cleanupFunc
        self.logFmtFunc = logFmtFunc
        self.printFmtFunc = printFmtFunc

    def startLogFile(self, filename, logFmtFunc):
        self.logFmtFunc = logFmtFunc
        self.logfile = open(filename, "w")
        for line in self.unloggedLines:
            self.logfile.write(line)
        self.unloggedLines = []

    def init(self):
        if self.initFunc:
            self.initFunc()

    def cleanup(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
        if self.cleanupFunc:
            self.cleanupFunc()

    def requestHandler(self, logentry):
        if logentry.doprint:
            print self.printFmtFunc(logentry)

        if self.logfile and self.logFmtFunc:
            text = self.logFmtFunc(logentry)
            if self.logfile:
                self.logfile.write(text)
            else:
                self.unloggedLines.append(text)

    def request(self, data, entrytype = _ENTRY_TYPE_.INFO, doprint = True):
        logentry = _LogEntry_(entrytype, data, doprint)
        QueueThread.request(self, logentry, callback = self.requestHandler)
        
###############################################################################
# Plain Text Helpers
###############################################################################

def formatTimestamp(timestamp = None):
    if not timestamp:
        timestamp = time.time()
    return (time.strftime("%Y-%m-%dT%H:%M:%S.",  time.localtime(timestamp)) +
            "%06d" %(1000000* (timestamp - int(timestamp))))

def _plaintextLogFmtFunc_(logentry):
    timestamp = formatTimestamp(logentry.timestamp)
    
    try:
        abrv = _LOG_ABRV_[logentry.entrytype]
    except LookupError as e:
        abrv = _LOG_ABRV_[_ENTRY_TYPE_.INFO]

    result = ""
    for line in str(logentry.data).split("\n"):
        result = result + "[%s] %s %s\n" %(timestamp, abrv, line)

    return result
                              
def _consolePrintFmtFunc_(logentry):
    timestamp = formatTimestamp(logentry.timestamp)
    
    try:
        fmt = _PRINT_COLOR_[logentry.entrytype]
    except LookupError as e:
        fmt = _PRINT_COLOR_[_ENTRY_TYPE_.INFO]
        
    result = ""
    prefix = ""
    for line in str(logentry.data).split("\n"):
        result = result + "%s[%s] %s" %(prefix, timestamp, fmt %(line))
        prefix = "\n"

    return result

def _plaintextRequest_(data, entrytype = _ENTRY_TYPE_.INFO, doprint = True):
    global _log_
    if not _log_:
        raise LoggerInitError()
    _log_.request(str(data), entrytype, doprint)

###############################################################################
# Module API
###############################################################################

_log_ = _LogWorker_(printFmtFunc = _consolePrintFmtFunc_)
_request_ = _plaintextRequest_
_log_.start()

def startPlaintextLog(filename):
    global _log_
    global _request_
    _log_.startLogFile(filename, _plaintextLogFmtFunc_)
    _request_ = _plaintextRequest_

def info(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.INFO, doprint = False)

def info(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.INFO)

def success(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.SUCCESS)

def bold(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.BOLD)

def warn(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.WARN)

def error(data):
    global _request_
    if not _request_:
        raise LoggerInitError()
    _request_(data, _ENTRY_TYPE_.ERROR)

# Join the thread before returning so that the log can empty its queue
def stop(timeout = 5):
    global _log_
    _log_.stop()
    _log_.join(timeout = timeout)

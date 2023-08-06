import threading
import Queue
import time

_SLEEP_TIME = 0.01

class LoopingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopFlag = threading.Event()

    def stop(self):
        self.stopFlag.set()

    def init(self):
        pass

    def worker(self):
        pass

    def cleanup(self):
        pass

    def proceed(self):
        return not self.stopFlag.isSet()

    def run(self):
        self.init()
        self.stopFlag.clear()
        while self.proceed():
            self.worker()
        self.stop()
        self.cleanup()

class _BlockingResponse:
    def __init__(self):
        self.data = None
        self.recvFlag = threading.Event()
        self.recvFlag.clear()

    def callback(self, data):
        self.data = data
        self.recvFlag.set()

    def getData(self, timeout = None):
        if timeout:
            endTime = time.time() + timeout
        while not timeout or time.time() < endTime:
            if self.recvFlag.isSet():
                break
            try:
                time.sleep(_SLEEP_TIME)
            except (KeyboardInterrupt, SystemExit) as e:
                raise e
            except:
                pass
        return self.data

class QueueThread(LoopingThread):
    def __init__(self, finishBeforeStop = False):
        self.finishBeforeStop = finishBeforeStop
        LoopingThread.__init__(self)
        self.seqn = 0
        self.queue = Queue.Queue()
        self.callbacksLock = threading.Lock()
        self.callbacks = {}

    # Modify the proceed function so that the thread can finish
    # processing everything before stopping
    def proceed(self):
        return (LoopingThread.proceed(self) or
                (self.finishBeforeStop and not self.queue.empty()))
        
    def request(self, data, callback = None, block = False, timeout = None):
        if self.stopFlag.isSet():
            return None

        resp = None
        if block:
            resp = _BlockingResponse()
            callback = resp.callback

        self.callbacksLock.acquire()
        self.callbacks[self.seqn] = callback
        self.callbacksLock.release()
        self.queue.put((self.seqn,data))
        self.seqn = self.seqn + 1

        if block:
            return resp.getData(timeout)

    def worker(self):
        if self.queue.empty():
            try:
                time.sleep(_SLEEP_TIME)
            except (KeyboardInterrupt, SystemExit) as e:
                raise e
            except:
                pass
            return
        
        seqn, data = self.queue.get(block=False)
        
        callback = None
        self.callbacksLock.acquire()
        if seqn in self.callbacks:
            callback = self.callbacks[seqn]
        self.callbacksLock.release()
                            
        if callback:
            callback(data)
            self.callbacksLock.acquire()
            self.callbacks[seqn] = None
            self.callbacksLock.release()
        

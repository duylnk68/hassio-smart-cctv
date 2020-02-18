import threading
import queue
from obj_detect import ObjDetect
import time

class ObjDetectPool:
    _modelFile = None
    _configFile = None
    _unprocessedQueue = queue.Queue()
    _resultDict = dict()

    def __init__(self, threadCount, modelFile, configFile):
        self._modelFile = modelFile
        self._configFile = configFile
        for id in range(threadCount):
            threading.Thread(target=self._ThreadProc, args=(id,)).start()

    def _ThreadProc(self, thread_id):
        objDetect = ObjDetect(self._modelFile, self._configFile)
        while True:
            data_id, data = self._unprocessedQueue.get()
            #data = objDetect.Detect(data)
            if data is None:
                continue
            self._resultDict[data_id].append(data)

    def Detect(self, data_id, data):
        if data_id not in self._resultDict:
            self._resultDict[data_id] = []
        self._unprocessedQueue.put((data_id, data))
        return

    def GetResults(self):
        result = dict()
        for key in self._resultDict:
            result[key] = self._resultDict[key]
            self._resultDict[key] = []
        return result
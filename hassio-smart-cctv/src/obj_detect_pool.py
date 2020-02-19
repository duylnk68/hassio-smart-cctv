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
            name, image, detect_list = self._unprocessedQueue.get()
            image = objDetect.Detect(image, detect_list)
            if image is None:
                continue
            self._resultDict[name].append(image)

    def Detect(self, name, image, detect_list):
        if name not in self._resultDict:
            self._resultDict[name] = []
        self._unprocessedQueue.put((name, image, detect_list))
        return

    def GetResults(self):
        result = dict()
        for name in self._resultDict:
            result[name] = self._resultDict[name]
            self._resultDict[name] = []
        return result
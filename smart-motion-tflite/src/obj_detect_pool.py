import threading
import queue
from obj_detect import ObjDetect
import time

class ObjDetectPool:
    _ModelFile = None
    _LabelFile = None
    _Threshold = 0.4
    _UnprocessedQueue = queue.Queue()
    _ResultDict = dict()
    _JpegQuality = 0

    def __init__(self, threadCount, modelFile, labelFile, threshold, jpegQuality):
        self._ModelFile = modelFile
        self._LabelFile = labelFile
        self._Threshold = threshold
        self._JpegQuality = jpegQuality
        for id in range(threadCount):
            threading.Thread(target=self._ThreadProc, args=(id,)).start()

    def _ThreadProc(self, thread_id):
        objDetect = ObjDetect(self._ModelFile, self._LabelFile, self._Threshold, self._JpegQuality)
        while True:
            name, image, detect_list = self._UnprocessedQueue.get()
            image = objDetect.Detect(image, detect_list)
            if image is None:
                continue
            self._ResultDict[name].append(image)

    def Detect(self, name, image, detect_list):
        if name not in self._ResultDict:
            self._ResultDict[name] = []
        self._UnprocessedQueue.put((name, image, detect_list))
        return

    def GetResults(self):
        result = dict()
        for name in self._ResultDict:
            result[name] = self._ResultDict[name]
            self._ResultDict[name] = []
        return result
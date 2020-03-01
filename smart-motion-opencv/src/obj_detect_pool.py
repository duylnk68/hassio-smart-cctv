import threading
import queue
from obj_detect import ObjDetect
import time

class ObjDetectPool:
    _PbFile = None
    _PbTxtFile = None
    _LabelFile = None
    _Threshold = 0.5
    _UnprocessedQueue = queue.Queue()
    _ResultDict = dict()
    _JpegQuality = 0

    def __init__(self, instances, pb_file, pbtxt_file, label_file, threshold, jpeg_quality):
        self._PbFile = pb_file
        self._PbTxtFile = pbtxt_file
        self._LabelFile = label_file
        self._Threshold = threshold
        self._JpegQuality = jpeg_quality
        for id in range(instances):
            threading.Thread(target=self._ThreadProc, args=(id,)).start()

    def _ThreadProc(self, thread_id):
        objDetect = ObjDetect(self._PbFile, self._PbTxtFile, self._LabelFile, self._Threshold, self._JpegQuality)
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
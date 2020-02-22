import cv2
import numpy as np

class ObjDetect:
    # Pretrained classes in the model
    _ClassNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
    _Model = None
    _JpegQuality = 95 # OpenCV default value

    # Get class_name from class_id
    def id_class_name(self, class_id):
        for key, value in self._ClassNames.items():
            if class_id == key:
                return value

    def __init__(self, modelFile, configFile, jpegQuality):
        # Loading model
        self._Model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
        if jpegQuality > 0:
            self._JpegQuality = jpegQuality
    
    def Detect(self, image_bytes, detect_list):
        image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), -1)
        image_height, image_width, _ = image.shape
        self._Model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
        output = self._Model.forward()
        isDetected = False
        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > .5:
                class_name = self.id_class_name(detection[1])
                if class_name in detect_list:
                    isDetected = True
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
                    cv2.putText(image, class_name,(int(box_x), int(box_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255)) 
        if isDetected is True:
            _, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), self._JpegQuality])
            return buffer.tobytes()
        return None


def test_ObjDetect():
    objDetect = ObjDetect("frozen_inference_graph.pb", "frozen_inference_graph.pbtxt", 0)
    with open("sample.jpeg", "rb") as in_file, open("result.jpeg", "wb") as out_file:
        detected_image = objDetect.Detect(in_file.read(), objDetect._ClassNames.values())
        if detected_image is not None:
            out_file.write(detected_image)

if __name__ == "__main__":
    test_ObjDetect()
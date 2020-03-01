import cv2
import numpy as np
import re

class ObjDetect:
    # Pretrained classes in the model
    _labels = None
    _model = None
    _thresold = 0.5
    _jpeg_quality = 95 # OpenCV default value

    def __init__(self, pb_file, pbtxt_file, label_file, threshold, jpeg_quality):
        # Load labels
        self._labels = self.load_labels(label_file)
        # Loading model
        self._model = cv2.dnn.readNetFromTensorflow(pb_file, pbtxt_file)
        if jpeg_quality > 0:
            self._jpeg_quality = jpeg_quality
        if threshold > 0:
            self._Thresold = threshold
    
    def load_labels(self, path):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels
    
    def Detect(self, image_bytes, detect_list):
        image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), -1)
        image_height, image_width, _ = image.shape
        self._model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
        output = self._model.forward()
        isDetected = False
        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > self._thresold:
                class_name = self._labels[detection[1]]
                if class_name in detect_list:
                    isDetected = True
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (0, 0, 255), thickness=1)
                    cv2.putText(image, class_name,(int(box_x), int(box_height) + 12), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255)) 
        if isDetected is True:
            _, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), self._jpeg_quality])
            return buffer.tobytes()
        return None


def test_ObjDetect():
    objDetect = ObjDetect("frozen_inference_graph.pb", "frozen_inference_graph.pbtxt", "coco_labels.txt", .5, 80)
    with open("sample.jpeg", "rb") as in_file, open("result.jpeg", "wb") as out_file:
        detected_image = objDetect.Detect(in_file.read(), objDetect._labels.values())
        if detected_image is not None:
            out_file.write(detected_image)

if __name__ == "__main__":
    test_ObjDetect()
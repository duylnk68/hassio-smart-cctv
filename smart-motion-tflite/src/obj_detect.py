# Reference from:
# => https://github.com/tensorflow/examples/blob/master/lite/examples/object_detection/raspberry_pi/detect_picamera.py
#
# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import numpy as np

from PIL import Image, ImageDraw
from tflite_runtime.interpreter import Interpreter

class ObjDetect:
    _labels = None
    _interpreter = None
    _threshold = 0.5
    _input_width = 0
    _input_height = 0
    _jpeg_quality = 95 # OpenCV default value

    def __init__(self, model_file, label_file, threshold, jpeg_quality):
        self._threshold = threshold
        self._labels = self.load_labels(label_file)
        self._interpreter = Interpreter(model_file)
        self._interpreter.allocate_tensors()
        _, self._input_width, self._input_height, _ = self._interpreter.get_input_details()[0]['shape']
        self._jpeg_quality = jpeg_quality

    def Detect(self, image_bytes, detect_list):
        original_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = original_image.resize((self._input_width, self._input_height), Image.ANTIALIAS)
        results = self.detect_objects(image)
        CAMERA_WIDTH, CAMERA_HEIGHT = original_image.size
        draw = ImageDraw.Draw(original_image)
        has_objects = False
        for obj in results:
            # Check class_name is in detect_list?
            class_name = self._labels[obj['class_id']]
            if class_name not in detect_list:
                # Skip draw bouding box
                continue
            else:
                # Set hasObjects to True
                has_objects = True

            # Convert the bounding box figures from relative coordinates
            # to absolute coordinates based on the original resolution
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * CAMERA_WIDTH)
            xmax = int(xmax * CAMERA_WIDTH)
            ymin = int(ymin * CAMERA_HEIGHT)
            ymax = int(ymax * CAMERA_HEIGHT)

            # Overlay the box, label, and score on the camera preview
            score = obj['score'] * 100
            draw.rectangle([xmin, ymin, xmax, ymax], outline ="red")
            draw.text([xmin, ymax], '{}:{:.2f}%'.format(self._labels[obj['class_id']], score), fill="red")
        del draw
        
        if has_objects:
            image_bytes_array = io.BytesIO()
            original_image.save(image_bytes_array, format='JPEG', quality=self._jpeg_quality, subsampling=0)
            return image_bytes_array.getvalue()
        else:
            return None

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


    def set_input_tensor(self, image):
        """Sets the input tensor."""
        tensor_index = self._interpreter.get_input_details()[0]['index']
        input_tensor = self._interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def get_output_tensor(self, index):
        """Returns the output tensor at the given index."""
        output_details = self._interpreter.get_output_details()[index]
        tensor = np.squeeze(self._interpreter.get_tensor(output_details['index']))
        return tensor


    def detect_objects(self, image):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(image)
        self._interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(0)
        classes = self.get_output_tensor(1)
        scores = self.get_output_tensor(2)
        count = int(self.get_output_tensor(3))

        results = []
        for i in range(count):
            if scores[i] >= self._threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i] }
                results.append(result)
        return results

def test():
    objDetect = ObjDetect("model.tflite", "coco_labels.txt", 0.6, 80)
    with open("sample.jpeg", "rb") as in_file, open("result.jpeg", "wb") as out_file:
        detected_image = objDetect.Detect(in_file.read(), objDetect._labels.values())
        if detected_image is not None:
            out_file.write(detected_image)

if __name__ == '__main__':
  test()

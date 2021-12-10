# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2021-12-09 11:24:00
# @Last Modified by:   Your name
# @Last Modified time: 2021-12-09 11:24:25
import tensorflow as tf
from tensorflow.python.eager.context import PhysicalDevice
from utils import load_class_names, output_boxes, draw_outputs, resize_image
import cv2
import numpy as np
from yolov3 import YOLOv3Net
# import os
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"    


PhysicalDevice = tf.config.experimental.list_physical_devices('GPU')
assert len(PhysicalDevice) > 0, "Not enough GPU hardware devices"
tf.config.experimental.set_memory_growth(PhysicalDevice[0], True)


class ImageDetector:
    def __init__(self):
        self.model_size = (416, 416, 3)
        self.num_classes = 80
        self.class_name = './data/coco.names'
        self.max_output_size = 40
        self.max_output_size_per_class= 20
        self.iou_threshold = 0.5
        self.confidence_threshold = 0.5

        self.cfgfile = 'cfg/yolov3.cfg'
        self.weightfile = 'weights/yolov3_weights.h5'

        self.model = YOLOv3Net(self.cfgfile, self.model_size, self.num_classes)
        self.model.load_weights(self.weightfile)

        self.class_names = load_class_names(self.class_name)
        
    def predict(self, filename):
        try:
            image = cv2.imread(filename)
            image = np.array(image)
            image = tf.expand_dims(image, 0)

            resized_frame = resize_image(image, (self.model_size[0], self.model_size[1]))
            pred = self.model.predict(resized_frame)

            boxes, scores, classes, nums = output_boxes(
                pred, self.model_size,
                max_output_size=self.max_output_size,
                max_output_size_per_class=self.max_output_size_per_class,
                iou_threshold=self.iou_threshold,
                confidence_threshold=self.confidence_threshold)

            image = np.squeeze(image)
            img = draw_outputs(image, boxes, scores, classes, nums, self.class_names)

            # If you want to save the result, uncommnent the line below:
            cv2.imwrite('result/test-images.jpg', img)
        except:
            print("File did not exist")
            return None

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import cv2
import numpy

class Detection(object):

    def __init__(self, input_path, fix_size=False, threshold=100):
        logging.info("processing {0}".format(input_path))
        self.input_path = input_path
        self.input_image = cv2.imread(self.input_path)

        if fix_size:
            self.__fix_image_size()
        
        self.blur_map, self.score, self.blurry = self.__estimate_blur(threshold)

        logging.info("input_path: {0}, score: {1}, blurry: {2}".format(self.input_path, self.score, self.blurry))

    def __fix_image_size(self, expected_pixels=2E6):
        image = self.input_image
        ratio = float(expected_pixels) / float(image.shape[0] * image.shape[1])
        self.input_image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)
        return 

    def __estimate_blur(self, threshold):
        if self.input_image.ndim == 3:
            image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)

        blur_map = cv2.Laplacian(self.input_image, cv2.CV_64F)
        score = numpy.var(blur_map)
        blurry = bool(score < threshold)
        return blur_map, score, blurry


    def pretty_blur_map(self, sigma=5):
        abs_image = numpy.log(numpy.abs(self.blur_map).astype(numpy.float32))
        cv2.blur(abs_image, (sigma, sigma))
        return cv2.medianBlur(abs_image, sigma)

    def get_result(self):
        return {"blurry": self.blurry,
                "input_path": self.input_path,
                "score": self.score}
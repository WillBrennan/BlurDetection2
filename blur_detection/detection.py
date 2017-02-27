#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import cv2
import numpy


def fix_image_size(image, expected_pixels=2E6):
    ratio = float(expected_pixels) / float(image.shape[0] * image.shape[1])
    return cv2.resize(image, (0, 0), fx=ratio, fy=ratio)


def estimate_blur(image, threshold=100):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    score = numpy.var(blur_map)
    return blur_map, score, bool(score < threshold)


def pretty_blur_map(blur_map, sigma=5):
    abs_image = numpy.log(numpy.abs(blur_map).astype(numpy.float32))
    cv2.blur(abs_image, (sigma, sigma))
    return cv2.medianBlur(abs_image, sigma)

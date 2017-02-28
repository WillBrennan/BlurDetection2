#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import logging

import cv2
import numpy

from blur_detection import estimate_blur
from blur_detection import fix_image_size
from blur_detection import pretty_blur_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run blur detection on a single image')
    parser.add_argument('-i', '--input_image', dest="input_image", type=str, required=True, help="directory of images")
    # parameters
    parser.add_argument("-t", "--threshold", dest='threshold', type=float, default=100.0, help="blurry threshold")
    parser.add_argument("-f", "--fix_size", dest="fix_size", help="fix the image size", action="store_true")
    # options
    parser.add_argument("-v", "--verbose", dest='verbose', help='set logging level to debug', action="store_true")
    parser.add_argument("-d", "--display", dest='display', help='display images', action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    assert os.path.exists(args.input_image)

    input_image = cv2.imread(args.input_image)

    if args.fix_size:
        input_image = fix_image_size(input_image)

    blur_map, score, blurry = estimate_blur(input_image)

    logging.info("score: {0}, blurry: {1}".format(score, blurry))

    if args.display:
        cv2.imshow("input", input_image)
        cv2.imshow("result", pretty_blur_map(blur_map))
        cv2.waitKey(0)

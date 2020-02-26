import sys
import argparse
import logging
import pathlib
import json

import cv2

from blur_detection import estimate_blur
from blur_detection import fix_image_size
from blur_detection import pretty_blur_map


def parse_args():
    parser = argparse.ArgumentParser(description='run blur detection on a single image')
    parser.add_argument('-i', '--images', type=str, nargs='+', required=True, help='directory of images')
    parser.add_argument('-s', '--save-path', type=str, default=None, help='path to save output')

    parser.add_argument('-t', '--threshold', type=float, default=100.0, help='blurry threshold')
    parser.add_argument('-f', '--variable-size', action='store_true', help='fix the image size')

    parser.add_argument('-v', '--verbose', action='store_true', help='set logging level to debug')
    parser.add_argument('-d', '--display', action='store_true', help='display images')

    return parser.parse_args()


def find_images(image_paths, img_extensions=['.jpg', '.png', '.jpeg']):
    img_extensions += [i.upper() for i in img_extensions]

    for path in image_paths:
        path = pathlib.Path(path)

        if path.is_file():
            if path.suffix not in img_extensions:
                logging.info(f'{path.suffix} is not an image extension! skipping {path}')
                continue
            else:
                yield path

        if path.is_dir():
            for img_ext in img_extensions:
                yield from path.rglob(f'*{img_ext}')


if __name__ == '__main__':
    assert sys.version_info >= (3, 6), sys.version_info
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    fix_size = not args.variable_size
    logging.info(f'fix_size: {fix_size}')

    if args.save_path is not None:
        save_path = pathlib.Path(args.save_path)
        assert save_path.suffix == '.json', save_path.suffix
    else:
        save_path = None

    results = []

    for image_path in find_images(args.images):
        image = cv2.imread(str(image_path))
        if image is None:
            logging.warning(f'warning! failed to read image from {image_path}; skipping!')
            continue

        logging.info(f'processing {image_path}')

        if fix_size:
            image = fix_image_size(image)
        else:
            logging.warning('not normalizing image size for consistent scoring!')

        blur_map, score, blurry = estimate_blur(image, threshold=args.threshold)

        logging.info(f'image_path: {image_path} score: {score} blurry: {blurry}')
        results.append({'input_path': str(image_path), 'score': score, 'blurry': blurry})

        if args.display:
            cv2.imshow('input', image)
            cv2.imshow('result', pretty_blur_map(blur_map))

            if cv2.waitKey(0) == ord('q'):
                logging.info('exiting...')
                exit()

    if save_path is not None:
        logging.info(f'saving json to {save_path}')

        with open(save_path, 'w') as result_file:
            data = {'images': args.images, 'threshold': args.threshold, 'fix_size': fix_size, 'results': results}
            json.dump(data, result_file, indent=4)

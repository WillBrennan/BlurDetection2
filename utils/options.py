import json
import argparse
import logging
from pathlib import Path

class Options(object):
    def __init__(self):

        self.__args = self.__build()

        self.threshold = self.__args.threshold
        self.fix_size = self.__args.fix_size
        
        self.logging_mode = self.__checkLogging()
        self.imgs = self.__find_images()

        self.__results = list()

    def __build(self):

        parser = argparse.ArgumentParser(description='run blur detection on a single image')

        # paths
        parser.add_argument('-i', '--input_dir', dest="input_dir", type=str, required=True, help="directory of images or a single image")
        parser.add_argument('-s', '--save_path', dest='save_path', type=str, required=True, help="path to save output")

        # parameters
        parser.add_argument("-t", "--threshold", dest='threshold', type=float, default=30.0, help="blurry threshold")
        parser.add_argument("-f", "--fix_size", dest="fix_size", help="fix the image size", action="store_true")

        # options
        parser.add_argument("-v", "--verbose", dest='verbose', help='set logging level to debug', action="store_true")

        args = parser.parse_args()
        return args

    def __checkLogging(self):
        if self.__args.verbose:
            logging.basicConfig(level=logging.DEBUG)
            return 'DEBUG'
        else:
            logging.basicConfig(level=logging.INFO)
            return 'INFO'

    def __find_images(self):
        path = Path(self.__args.input_dir)
        imgtypes = 'jpg, png, jpeg'
        if path.is_dir():
            imgs = [img.as_posix() for img in path.glob('./*.*[{}]'.format(imgtypes))]
            assert len(imgs) == 0, 'The directory cannot find any images.'
            return imgs
        else:
            suffix_check = True if imgtypes.find(path.suffix[1:]) > 0 else False
            assert suffix_check, 'Please check the type of input image.'
            exist_check = path.is_file() 
            if exist_check:
                return [path.as_posix()]
            else:
                assert exist_check, '"{}" is not found.'.format(path)

    def save_result(self):
        logging.info("writing results to {0}".format(self.__args.save_path))

        assert Path(self.__args.save_path).suffix == ".json"

        with open(self.__args.save_path, 'w') as outfile:
            data = {"input_dir": self.__args.input_dir, 
                    "threshold": self.__args.threshold, 
                    "results": self.__results}
            json.dump(data, outfile, sort_keys=True, indent=4)
            outfile.write("\n")

    def add_result(self, data):
        self.__results.append(data)

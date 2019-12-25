#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import (Options, Detection)

if __name__ == '__main__':
    
    opt = Options()

    for input_path in opt.imgs:
        try:
            d = Detection(input_path, opt.fix_size, opt.threshold)
            opt.add_result(d.get_result())
        except Exception as e:
            print(e)
            pass

    opt.save_result()
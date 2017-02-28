# Blur Detection
Blur Detection works using the total variance of the laplacian of an
image, this provides a quick and accurate method for scoring how blurry
an image is.


The repository has two main scripts, `single.py` and `batch.py`, which
use the same blur detection method located in `blur_detection`. The
blur detection method is highly dependent on the size of the image
being processed. To get consistent scores the `-f` argument can be used
to resize the image.

```bash
# processing a single image
python single.py -i input_image.py -d -f

# processing a directory
python batch.py -i input_directory/ -s results.json -f
```

The `batch.py` script produces a json file with information on the
how blurry an image is, the higher the value, the less blurry the image.

```json
{
    "input_dir": "/Users/demo_user/Pictures/Flat/",
    "results": [
        {
            "blurry": false,
            "input_path": "/Users/demo_user/Pictures/Flat/IMG_1666.JPG",
            "score": 6984.8082115095549
        },
    ],
    "threshold": 100.0
}
```


![Blur Mask Demo](https://raw.githubusercontent.com/WillBrennan/BlurDetection/master/docs/demo.png)
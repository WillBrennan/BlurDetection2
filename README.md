# Blur Detection

Blur Detection works using the total variance of the laplacian of an
image, this provides a quick and accurate method for scoring how blurry
an image is.

The blur detection method is highly dependent on the size of the image
being processed. To get consistent scores the `-f` argument can be used
to resize the image.

## Usage

```bash
# processing a directory or a single image
python main.py -i <YOUR_INPUT> -s results.json -f
```

## Result

The `main.py` script produces a json file with information on the
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

## Reference

This is based upon the blogpost [Blur Detection With Opencv](https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/) by Adrian Rosebrock.

![Blur Mask Demo](https://raw.githubusercontent.com/WillBrennan/BlurDetection2/master/docs/demo.png)

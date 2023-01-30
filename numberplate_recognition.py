import os
import sys
from pathlib import Path

import pytesseract
from cv2 import VideoCapture, imwrite

# when running on windows import tesseract like this
# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


# whether not to save images from predictions
NOSAVE = True

# path of this file
FILE = Path(__file__).resolve()
# YOLOv5 root directory
ROOT = FILE.parents[0]
YOLO = ROOT / "yolov5"
if str(ROOT) not in sys.path:
    # add ROOT to PATH
    sys.path.append(str(ROOT))
if str(YOLO) not in sys.path:
    # add ROOT to PATH
    sys.path.append(str(YOLO))
# relative
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))

# can import just when path contains YOLO dir
from yolov5.utils.general import increment_path
from yolov5.detect import run


def detect_numberplate():
    # increment exp dirs
    save_dir = increment_path(Path(YOLO / "runs/detect/exp"), mkdir=True)
    # path for taken image
    file_path = str(save_dir) + "/image.jpg"

    cam = VideoCapture(0)
    # take image
    result, image = cam.read()

    # close cam
    cam.release()

    if result:  # if image will detected without any error show result
        imwrite(file_path, image)  # saving image in local storage
        detect_results = run(weights=YOLO / 'runs/train/yolov5s_results/weights/best.onnx',
                             imgsz=(416, 416),
                             source=save_dir,
                             nosave=NOSAVE
                             )  # start ai detection
        # remove image after detection
        if NOSAVE and os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("images saved to: " + str(save_dir))

        # if there were numerplates detected
        if detect_results:
            # convert picture to text
            text_results = convert_to_text(
                detect_results)
            # clean test_results
            cleaned_text_results = list(
                map(clean, text_results))
            # print results when started manually
            if __name__ == "__main__":
                print(cleaned_text_results)
            else:
                return cleaned_text_results
        else:
            print("no numberplate detected on the image")
    # If captured image is corrupted, moving to else part
    else:
        print("no image detected")

    # return empty string when nothin was detected
    return ""


def clean(result):
    """remove escape characters and whitespaces"""
    return "".join(result.split())


def convert_to_text(detect_results):
    """get the text from the detection result images"""
    text_results = []
    for result in detect_results:
        try:
            text_results.append(pytesseract.image_to_string(
                result, config='--oem 0 --psm 11 -c tessedit_char_whitelist=ÄÖÜABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            )
        except Exception as e:
            print(e)
    return text_results

# for manual use
if __name__ == "__main__":
    detect_numberplate()

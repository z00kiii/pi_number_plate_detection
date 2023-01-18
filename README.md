Installation on Raspberry Pi 4
1. currently tested on debian buster 64 bit and python 3.7 (https://forums.raspberrypi.com/viewtopic.php?f=117&t=275370)
2. install requirements in rodamaati and in yolo directory (if there are problems with torch: https://github.com/pytorch/vision/issues/5919#issuecomment-1142350615, works with torch 1.10.0 and torchvision 0.11.1)
3. run "sudo apt update -y"
4. run "sudo apt install tesseract-ocr" and "sudo apt install libtesseract-dev" (https://github.com/tesseract-ocr/tesseract/issues/1799#issuecomment-632740838)
5. update tesseract to v5 (maybe by: https://techviewleo.com/install-and-use-tesseract-ocr-on-debian/)
6. exchange file eng.traineddata in "/usr/share/tesseract-ocr/5/tessdata/" with current on git via "wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata" answered here: (https://stackoverflow.com/a/49030935/18002090)
7. run sensor.py to start the app

8. for autostart setup systemd service
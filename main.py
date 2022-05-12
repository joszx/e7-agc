import cv2 as cv
import numpy as np
import os
import time
import cv2
import pytesseract
#from time import time
from windowcapture import WindowCapture
from ctypes import windll
from PIL import Image


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Make program aware of DIP scaling e.g. monitor 1 - 125%, monitor 2 - 100%
# Credit: https://stackoverflow.com/questions/40869982/dpi-scaling-level-affecting-win32gui-getwindowrect-in-python
user32 = windll.user32
user32.SetProcessDPIAware()

# WindowCapture.list_window_names()
# exit()

# initialize the WindowCapture class
wincap = WindowCapture('LDPlayer')

loop_time = time.time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    screenshot = cv2.rectangle(screenshot, (875, 125), (1100, 225), (0,255,0), 2)
    screenshot = cv2.rectangle(screenshot, (475, 525), (822, 650), (0,255,0), 2)

    # crop screenshot image by height then by width, Y then X
    equip_region =  screenshot[125:225,875:1100]
    substat_region = screenshot[525:650,475:822]

    cv.imshow('Computer Vision', screenshot)
    cv.imshow('CV equip region', equip_region)
    cv.imshow('CV substat region', substat_region)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    myconfig = r"--psm 3 --oem 0"
    text = pytesseract.image_to_string(equip_region, config=myconfig, output_type=pytesseract.Output.DICT)
    print(text)


    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    time.sleep(1)


print('Done.')
import cv2 as cv
import numpy as np
import os
import time
import pytesseract
#from time import time
from windowcapture import WindowCapture
from ctypes import windll
from PIL import Image
from parser import Parser


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

    screenshot = cv.rectangle(screenshot, Parser.EQUIPPED_BY_TOP_LEFT, Parser.EQUIPPED_BY_BOT_RIGHT, (0,255,0), 2)
    screenshot = cv.rectangle(screenshot, Parser.SUBSTAT_TOP_LEFT, Parser.SUBSTAT_BOT_RIGHT, (0,0,0), 2)

    # crop screenshot image by height then by width, Y then X
    equip_region =  screenshot[125:225,875:1100]
    substat_region = screenshot[Parser.SUBSTAT_TOP_LEFT[1]:Parser.SUBSTAT_BOT_RIGHT[1], Parser.SUBSTAT_TOP_LEFT[0]:Parser.SUBSTAT_BOT_RIGHT[0]]

    # turn substat region bw for tesseract better processing
    substat_region_grayscale = cv.cvtColor(substat_region, cv.COLOR_BGR2GRAY)
    (thresh, substat_region_bw) = cv.threshold(substat_region_grayscale, 64, 255, cv.THRESH_BINARY_INV)

    cv.imshow('Computer Vision', screenshot)
    cv.imshow('CV equip region', equip_region)
    cv.imshow('CV substat region', substat_region)
    cv.imshow('CV substat region grayscale', substat_region_grayscale)
    cv.imshow('CV black and white substat region', substat_region_bw)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    myconfig = r"--psm 3 --oem 3"
    # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
    equipped_by_text = pytesseract.image_to_string(equip_region, config=myconfig, output_type=pytesseract.Output.STRING)
    print(equipped_by_text)
    substat_text = pytesseract.image_to_string(substat_region_bw, config=myconfig, output_type=pytesseract.Output.STRING)
    print(substat_text)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    #time.sleep(1)


print('Done.')
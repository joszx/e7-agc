import cv2 as cv
import numpy
import time
import pytesseract
from windowcapture import WindowCapture
from ctypes import windll
from parser import Parser
from screengrabber import ScreenGrabber

# Constants
ORANGE_MIN = (5, 100, 50)
ORANGE_MAX = (15, 255, 255)


# Make program aware of DPI scaling e.g. monitor 1 - 125%, monitor 2 - 100%
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

    #screenshot = cv.rectangle(screenshot, Parser.EQUIPPED_BY_TOP_LEFT, Parser.EQUIPPED_BY_BOT_RIGHT, (0,255,0), 2)
    screenshot = cv.rectangle(screenshot, ScreenGrabber.SUBSTAT_TOP_LEFT, ScreenGrabber.SUBSTAT_BOT_RIGHT, (255,255,255), 2)
    screenshot = cv.rectangle(screenshot, ScreenGrabber.GEAR_INFO_TOP_LEFT, ScreenGrabber.GEAR_INFO_BOT_RIGHT, (255,255,255), 2)

    # crop screenshot image by height then by width, Y then X
    #equip_region =  screenshot[125:225,875:1100]
    substat_region = screenshot[ScreenGrabber.SUBSTAT_TOP_LEFT[1]:ScreenGrabber.SUBSTAT_BOT_RIGHT[1], ScreenGrabber.SUBSTAT_TOP_LEFT[0]:ScreenGrabber.SUBSTAT_BOT_RIGHT[0]]

    # filter out orange for substat region
    substat_region_hsv = cv.cvtColor(substat_region, cv.COLOR_BGR2HSV)
    orange_mask = cv.inRange(substat_region_hsv, ORANGE_MIN, ORANGE_MAX)
    invert_orange_mask = cv.bitwise_not(orange_mask) # maybe could be replaced with 255 - orange_mask

    substat_region_filtered_orange = cv.bitwise_and(substat_region, substat_region, mask=invert_orange_mask)

    # turn substat region bw for tesseract better processing
    substat_region_grayscale = cv.cvtColor(substat_region_filtered_orange, cv.COLOR_BGR2GRAY)
    (thresh, substat_region_bw) = cv.threshold(substat_region_grayscale, 30, 255, cv.THRESH_BINARY_INV)
    #substat_region_bw = cv.resize(substat_region_bw, None, fx=1.2, fy=1.2, interpolation=cv.INTER_CUBIC)

    # get gear info details
    gear_info_region = screenshot[ScreenGrabber.GEAR_INFO_TOP_LEFT[1]:ScreenGrabber.GEAR_INFO_BOT_RIGHT[1], ScreenGrabber.GEAR_INFO_TOP_LEFT[0]:ScreenGrabber.GEAR_INFO_BOT_RIGHT[0]]
    
    gear_info_region_hsv = cv.cvtColor(gear_info_region, cv.COLOR_BGR2HSV)
    gear_info_orange_mask = cv.inRange(gear_info_region_hsv, ORANGE_MIN, ORANGE_MAX)
    gear_info_invert_orange_mask = cv.bitwise_not(gear_info_orange_mask) # maybe could be replaced with 255 - orange_mask
    gear_info_filtered_orange = cv.bitwise_and(gear_info_region, gear_info_region, gear_info_invert_orange_mask)

    gear_info_grayscale = cv.cvtColor(gear_info_region, cv.COLOR_BGR2GRAY)
    (thresh, gear_info_bw) = cv.threshold(gear_info_grayscale, 100, 255, cv.THRESH_BINARY_INV)

    cv.imshow('Computer Vision', screenshot)
    #cv.imshow('CV equip region', equip_region)
    # cv.imshow('CV substat region', substat_region)
    # cv.imshow('CV substat region filter orange', substat_region_filtered_orange)
    # cv.imshow('CV substat region grayscale', substat_region_grayscale)
    cv.imshow('CV black and white substat region', substat_region_bw)
    cv.imshow('CV gear info region', gear_info_region)
    cv.imshow('Cv gear info filtered orange', gear_info_orange_mask)
    cv.imshow('CV gear info grayscale',gear_info_grayscale)
    cv.imshow('CV gear info bw', gear_info_bw)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    myconfig = r"--psm 6 --oem 3"
    # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
    #equipped_by_text = pytesseract.image_to_string(equip_region, config=myconfig, output_type=pytesseract.Output.STRING)
    #print(equipped_by_text)
    substat_text = pytesseract.image_to_string(substat_region_bw, config=myconfig, output_type=pytesseract.Output.STRING)
    print(substat_text)
    #gearinfo_text = pytesseract.image_to_string()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    #time.sleep(1)


print('Done.')
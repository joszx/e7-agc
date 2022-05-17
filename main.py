import cv2 as cv
import numpy
import time
import pytesseract
import screengrabber
from windowcapture import WindowCapture
from ctypes import windll
from parser import Parser

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

    screenshot = screengrabber.make_rectangle_around(screenshot, "substat text")
    screenshot = screengrabber.make_rectangle_around(screenshot, "substat roll")
    #screenshot = screengrabber.make_rectangle_around(screenshot, "gear level")

    # crop screenshot image by height then by width, Y then X
    substat_text_region = screengrabber.crop_image_around(screenshot, "substat text")
    substat_roll_region = screengrabber.crop_image_around(screenshot, "substat roll")


    # filter out orange for substat roll region
    substat_roll_region_filtered_orange = screengrabber.filter_orange_from_image(substat_roll_region)

    # turn substat region bw for tesseract better processing
    substat_text_region_bw = screengrabber.transform_image_bw(substat_text_region, 30)
    #substat_region_bw = screengrabber.upscale_image(substat_region_bw, 1.2)
    substat_roll_region_bw = screengrabber.transform_image_bw(substat_roll_region_filtered_orange, 30)

    # get gear info details
    gear_level_region = screengrabber.crop_image_around(screenshot, "gear level")

    gear_level_bw = screengrabber.transform_image_bw(gear_level_region, 175)

    cv.imshow('Computer Vision', screenshot)
    #cv.imshow('CV equip region', equip_region)
    # cv.imshow('CV substat region', substat_text_region)
    # cv.imshow('CV substat region filter orange', substat_region_filtered_orange)
    # cv.imshow('CV substat region grayscale', substat_region_grayscale)
    cv.imshow('CV substat roll region bw', substat_roll_region_bw)
    cv.imshow('CV black and white substat region', substat_text_region_bw)
    cv.imshow('CV gear level region', gear_level_region)
    cv.imshow('CV gear level bw', gear_level_bw)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    substat_text_config = r"-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ' --psm 6 --oem 3"
    substat_roll_config = r"-c tessedit_char_whitelist='1234567890%' --psm 6 --oem 3"
    gear_level_config = r'-c tessedit_char_whitelist=1234567890 --psm 8 --oem 3'
    # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
    #equipped_by_text = pytesseract.image_to_string(equip_region, config=substat_text_config, output_type=pytesseract.Output.STRING)
    #print(equipped_by_text)
    substat_text = pytesseract.image_to_string(substat_text_region_bw, config=substat_text_config, output_type=pytesseract.Output.STRING)
    print(substat_text)
    substat_roll = pytesseract.image_to_string(substat_roll_region_bw, config=substat_roll_config, output_type=pytesseract.Output.STRING)
    print(substat_roll)
    gear_level_text = pytesseract.image_to_string(gear_level_bw, config=gear_level_config, output_type=pytesseract.Output.STRING)
    print(gear_level_text)
    #gearinfo_text = pytesseract.image_to_string()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    #time.sleep(1)


print('Done.')
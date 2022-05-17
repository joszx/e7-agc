import cv2 as cv
import numpy
import time
import pytesseract
import screengrabber
from windowcapture import WindowCapture
from ctypes import windll


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

    #screenshot = cv.rectangle(screenshot, screengrabber.EQUIPPED_BY_TOP_LEFT, screengrabber.EQUIPPED_BY_BOT_RIGHT, (0,255,0), 2)
    #screenshot = cv.rectangle(screenshot, screengrabber.SUBSTAT_TOP_LEFT, screengrabber.SUBSTAT_BOT_RIGHT, (255,255,255), 3)
    #screenshot = cv.rectangle(screenshot, screengrabber.GEAR_LEVEL_TOP_LEFT, screengrabber.GEAR_LEVEL_BOT_RIGHT, (255,255,255), 1)

    # crop screenshot image by height then by width, Y then X
    #equip_region =  screenshot[125:225,875:1100]
    #substat_region = screenshot[screengrabber.SUBSTAT_TOP_LEFT[1]:screengrabber.SUBSTAT_BOT_RIGHT[1], screengrabber.SUBSTAT_TOP_LEFT[0]:screengrabber.SUBSTAT_BOT_RIGHT[0]]
    gear_level_region = screenshot[screengrabber.GEAR_LEVEL_TOP_LEFT[1]:screengrabber.GEAR_LEVEL_BOT_RIGHT[1], screengrabber.GEAR_LEVEL_TOP_LEFT[0]:screengrabber.GEAR_LEVEL_BOT_RIGHT[0]]


    # turn substat region bw for tesseract better processing
    # substat_region_grayscale = cv.cvtColor(substat_region, cv.COLOR_BGR2GRAY)
    # (thresh, substat_region_bw) = cv.threshold(substat_region_grayscale, 30, 255, cv.THRESH_BINARY_INV)
    # substat_region_bw = cv.resize(substat_region_bw, None, fx=1.2, fy=1.2, interpolation=cv.INTER_CUBIC)

    gear_level_region_grayscale = cv.cvtColor(gear_level_region, cv.COLOR_BGR2GRAY)
    (thresh, gear_level_region_bw) = cv.threshold(gear_level_region_grayscale, 175, 255, cv.THRESH_BINARY_INV)
    #gear_level_region_bw = cv.resize(gear_level_region_bw, None, fx=1.2, fy=1.2, interpolation=cv.INTER_CUBIC)

    cv.imshow('Computer Vision', screenshot)
    cv.imshow('CV gear level region', gear_level_region)
    cv.imshow('CV gear level region grayscale', gear_level_region_grayscale)
    cv.imshow('CV black and white gear level region', gear_level_region_bw)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    myconfig = r"--psm 6 --oem 3"
    custom_config = r'-c tessedit_char_whitelist=1234567890 --psm 8 --oem 3'
    # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
    #equipped_by_text = pytesseract.image_to_string(equip_region, config=myconfig, output_type=pytesseract.Output.STRING)
    #print(equipped_by_text)
    #substat_text = pytesseract.image_to_string(substat_region_bw, config=myconfig, output_type=pytesseract.Output.STRING)
    #print(substat_text)

    gear_level_text = pytesseract.image_to_string(gear_level_region_bw, config=custom_config, output_type=pytesseract.Output.STRING)
    print(gear_level_text)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    #time.sleep(1)


print('Done.')
import cv2 as cv
import time
import pytesseract
import screengrabber
import parser
from gear.gear import Gear
from windowcapture import WindowCapture
from ctypes import windll

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
    #screenshot = screengrabber.make_rectangle_around(screenshot, "gear enhance")
    #screenshot = screengrabber.make_rectangle_around(screenshot, "gear type")

    # crop screenshot image by height then by width, Y then X
    substat_text_region = screengrabber.crop_image_around(screenshot, "substat text")
    substat_roll_region = screengrabber.crop_image_around(screenshot, "substat roll")


    # filter out orange for substat roll region
    substat_roll_region_filtered_orange = screengrabber.filter_orange_from_image(substat_roll_region)

    # turn substat region bw for tesseract better processing
    substat_text_region_bw = screengrabber.transform_image_bw(substat_text_region, 30)
    substat_text_region_bw = screengrabber.upscale_image(substat_text_region_bw, 1.2)
    substat_roll_region_bw = screengrabber.transform_image_bw(substat_roll_region_filtered_orange, 100)

    # get gear info details
    gear_level_region = screengrabber.crop_image_around(screenshot, "gear level")
    gear_enhance_region = screengrabber.crop_image_around(screenshot, "gear enhance")
    gear_type_region = screengrabber.crop_image_around(screenshot, "gear type")

    gear_level_bw = screengrabber.transform_image_bw(gear_level_region, 175)
    gear_enhance_bw = screengrabber.transform_image_bw(gear_enhance_region, 200)
    gear_type_bw = screengrabber.transform_image_bw(gear_type_region, 30)



    cv.imshow('Computer Vision', screenshot)
    cv.imshow('CV substat roll region bw', substat_roll_region_bw)
    cv.imshow('CV black and white substat region', substat_text_region_bw)
    cv.imshow('CV gear level bw', gear_level_bw)
    cv.imshow('CV gear enhance bw', gear_enhance_bw)
    cv.imshow('CV gear type', gear_type_bw)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # tesseract ocr code
    substat_text_config = r"--psm 6 --oem 3"
    substat_roll_config = r"-c tessedit_char_whitelist='1234567890%' --psm 6 --oem 3" # LSTM detects 11 as 1 while tesseract detects % as 0 0
    gear_level_config = r'-c tessedit_char_whitelist=1234567890 --psm 8 --oem 3'
    gear_enhance_config = r"-c tessedit_char_whitelist='1234567890' --psm 8 --oem 3"
    gear_type_config = r"-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ' --psm 7 --oem 3"
    # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
    #equipped_by_text = pytesseract.image_to_string(equip_region, config=substat_text_config, output_type=pytesseract.Output.STRING)
    #print(equipped_by_text)
    substat_text = pytesseract.image_to_string(substat_text_region_bw, config=substat_text_config, output_type=pytesseract.Output.STRING)
    # print(substat_text)
    substat_roll = pytesseract.image_to_string(substat_roll_region_bw, config=substat_roll_config, output_type=pytesseract.Output.STRING)
    # print(substat_roll)
    gear_level_text = pytesseract.image_to_string(gear_level_bw, config=gear_level_config, output_type=pytesseract.Output.STRING)
    # print(gear_level_text)
    gear_enhance_text = pytesseract.image_to_string(gear_enhance_bw, config=gear_enhance_config, output_type=pytesseract.Output.STRING)
    # print(gear_enhance_text)
    gear_type_text = pytesseract.image_to_string(gear_type_bw, config=gear_type_config, output_type=pytesseract.Output.STRING)
    # print(gear_type_text)

    gear_level = parser.remove_newline(gear_level_text)
    gear_type = parser.parse_gear_type(parser.remove_newline(gear_type_text))
    gear_enhance_level = parser.parse_gear_enhance_level(parser.remove_newline(gear_enhance_text))
    substat_text = parser.str_to_list(substat_text)
    substat_roll = parser.str_to_list(substat_roll)
    substat_text, substat_roll = parser.parse_substats(substat_text, substat_roll)

    curr_gear = Gear(gear_level, gear_type, gear_enhance_level, substat_text, substat_roll)

    print(curr_gear)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

    time.sleep(0.5)


print('Done.')
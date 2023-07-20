import cv2 as cv
import time
import pytesseract
from myexception import GearParseException, GearLevelException
import screengrabber
import gearparser
from edgedetector import EdgeDetector
from gear.gear import Gear
from windowcapture import WindowCapture
from ctypes import windll

from tkinter import StringVar
import tkinter as tk
import threading

class logic:

    def initDPIAware(self):
        # Make program aware of DPI scaling e.g. monitor 1 - 125%, monitor 2 - 100%
        # Credit: https://stackoverflow.com/questions/40869982/dpi-scaling-level-affecting-win32gui-getwindowrect-in-python
        user32 = windll.user32
        user32.SetProcessDPIAware()

    def __init__(self):
        
        self.initDPIAware()

        # set tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract.exe'

        # Get list of all opened windows
        # WindowCapture.list_window_names()
        # exit()

        # initialize the WindowCapture class
        # wincap = WindowCapture('LDPlayer')
        wincap = WindowCapture('BlueStacks App Player')

        # initialize the edge detector class to detect entering into the enhance page
        enhance_page_detector = EdgeDetector()

        loop_time = time.time()
        while(True):

            # get an updated image of the game
            screenshot = wincap.get_screenshot()

            screenshot = screengrabber.make_rectangle_around(screenshot, "enhance equipment")

            enhance_equipment_region = screengrabber.crop_image_around(screenshot, "enhance equipment")
            enhance_equipment_bw = screengrabber.transform_image_bw(enhance_equipment_region, 50)
            enhance_equipment_config = r"-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ' --psm 6 --oem 3 "
            enhance_equipment_text = pytesseract.image_to_string(enhance_equipment_bw, config=enhance_equipment_config, output_type=pytesseract.Output.STRING)
            enhance_equipment_text = gearparser.remove_newline(enhance_equipment_text)

            # print(enhance_equipment_text)

            # cv.imshow('Enhance equipment region', enhance_equipment_region)
            # cv.imshow('Enhance equipment bw', enhance_equipment_bw)

            if enhance_equipment_text == 'Enhance Equipment' or enhance_equipment_text == 'Substat Modification':
                enhance_page_detector.update_value(True)
            else:
                enhance_page_detector.update_value(False)


            if enhance_page_detector.check_edge():

                # time delay for page to load after detecting enhance equipment page
                time.sleep(0.5)
                
                # renew screenshot to wait after enhance equipment page loads
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
                substat_roll_region_upscale = screengrabber.upscale_image(substat_roll_region_filtered_orange, 1.4)
                substat_roll_region_bw = screengrabber.transform_image_bw(substat_roll_region_upscale, 50)

                # get gear info details
                gear_level_region = screengrabber.crop_image_around(screenshot, "gear level")
                gear_enhance_region = screengrabber.crop_image_around(screenshot, "gear enhance")
                gear_type_region = screengrabber.crop_image_around(screenshot, "gear type")

                gear_level_bw = screengrabber.filter_for_color(gear_level_region)
                gear_level_bw = screengrabber.transform_image_bw(gear_level_bw, 150)
                gear_enhance_bw = screengrabber.transform_image_bw(gear_enhance_region, 200)
                gear_type_bw = screengrabber.transform_image_bw(gear_type_region, 30)



                # cv.imshow('Computer Vision', screenshot)
                # cv.imshow('CV substat roll region bw', substat_roll_region_bw)
                # cv.imshow('CV black and white substat region', substat_text_region_bw)
                # cv.imshow('CV gear level bw', gear_level_bw)
                # cv.imshow('CV gear enhance bw', gear_enhance_bw)
                # cv.imshow('CV gear type', gear_type_bw)

                # debug the loop rate
                # print('FPS {}'.format(1 / (time.time() - loop_time)))
                # loop_time = time.time()

                # tesseract ocr code
                substat_text_config = r"--psm 6 --oem 3"
                substat_roll_config = r"-c tessedit_char_whitelist='1234567890%' --psm 6 --oem 3" # LSTM detects 11 as 1 while tesseract detects % as 0 0
                gear_level_config = r'-c tessedit_char_whitelist=1234567890 --psm 11 --oem 3'
                gear_enhance_config = r"-c tessedit_char_whitelist='1234567890+' --psm 11 --oem 3"
                gear_type_config = r"-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ' --psm 11 --oem 3"
                # custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
                #equipped_by_text = pytesseract.image_to_string(equip_region, config=substat_text_config, output_type=pytesseract.Output.STRING)
                #print(equipped_by_text)
                substat_text = pytesseract.image_to_string(substat_text_region_bw, config=substat_text_config, output_type=pytesseract.Output.STRING)
                # print(substat_text)
                substat_roll = pytesseract.image_to_string(substat_roll_region_bw, config=substat_roll_config, output_type=pytesseract.Output.STRING)
                # print(substat_roll)
                gear_level_text = pytesseract.image_to_string(gear_level_bw, config=gear_level_config, output_type=pytesseract.Output.STRING)
                print(gear_level_text)
                gear_enhance_text = pytesseract.image_to_string(gear_enhance_bw, config=gear_enhance_config, output_type=pytesseract.Output.STRING)
                # print(gear_enhance_text)
                gear_type_text = pytesseract.image_to_string(gear_type_bw, config=gear_type_config, output_type=pytesseract.Output.STRING)
                # print(gear_type_text)
                
                try:
                    gear_level = gearparser.remove_newline(gear_level_text)
                    gear_type = gearparser.parse_gear_type(gearparser.remove_newline(gear_type_text))
                    gear_enhance_level = gearparser.parse_gear_enhance_level(gearparser.remove_newline(gearparser.remove_plussign(gear_enhance_text)))
                    substat_text = gearparser.str_to_list(substat_text)
                    print(substat_text)
                    print(substat_roll)
                    substat_roll = gearparser.str_to_list(substat_roll)
                    print(substat_roll)
                    substat_text, substat_roll = gearparser.parse_substats(substat_text, substat_roll)

                    curr_gear = Gear(gear_level, gear_type, gear_enhance_level, substat_text, substat_roll)
                    print(curr_gear)
                    out = curr_gear

                except GearParseException as e:
                    details = e.args[0]
                    out = "Error parsing gear\n" + details
                except GearLevelException as e:
                    details = e.args[0]
                    out = details
                except:
                    out = "Error initialising gear"


                outputstring.set(out)

            # press 'q' with the output window focused to exit.
            # waits 1 ms every loop to process key presses
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

            time.sleep(0.5)


# Create window object
window = tk.Tk()

window.title('e7-agc')
window.geometry('600x400')

frame = tk.Frame()
frame.pack()

bottomframe = tk.Frame()
bottomframe.pack(side=tk.BOTTOM)

outputstring = StringVar()
outputstring.set("default text")


output = tk.Label(
    bottomframe,
    textvariable=outputstring,
    font=("Arial", 15)
)


# Bind keypress event to handle_keypress()
# window.bind("<Key>", handle_keypress)
output.pack(side=tk.BOTTOM)

t1 = threading.Thread(target=logic, daemon=True)
t1.start()

# Start program
window.mainloop()
import cv2

# constants
EQUIPPED_BY_TOP_LEFT = (875, 125)
EQUIPPED_BY_BOT_RIGHT = (1100, 225)
EQUIPPED_BY_RECT = (EQUIPPED_BY_TOP_LEFT, EQUIPPED_BY_BOT_RIGHT)

SUBSTAT_TEXT_TOP_LEFT = (35, 400)
SUBSTAT_TEXT_BOT_RIGHT = (300, 530)
SUBSTAT_TEXT_RECT = (SUBSTAT_TEXT_TOP_LEFT, SUBSTAT_TEXT_BOT_RIGHT)
SUBSTAT_ROLL_TOP_LEFT = (300, 400)
SUBSTAT_ROLL_BOT_RIGHT = (450, 530)
SUBSTAT_ROLL_RECT = (SUBSTAT_ROLL_TOP_LEFT, SUBSTAT_ROLL_BOT_RIGHT)

GEAR_LEVEL_TOP_LEFT = (57, 181)
GEAR_LEVEL_BOT_RIGHT = (83, 201)
GEAR_LEVEL_RECT = (GEAR_LEVEL_TOP_LEFT, GEAR_LEVEL_BOT_RIGHT)
GEAR_ENHANCE_TOP_LEFT = (140, 165)
GEAR_ENHANCE_BOT_RIGHT = (165, 190)
GEAR_ENHANCE_RECT = (GEAR_ENHANCE_TOP_LEFT, GEAR_ENHANCE_BOT_RIGHT)
GEAR_TYPE_TOP_LEFT = (170, 180)
GEAR_TYPE_BOT_RIGHT = (350, 210)
GEAR_TYPE_RECT = (GEAR_TYPE_TOP_LEFT, GEAR_TYPE_BOT_RIGHT)

ENHANCE_PAGE_TOP_LEFT = (70, 50)
ENHANCE_PAGE_BOT_RIGHT = (430, 100)
ENHANCE_PAGE_RECT = (ENHANCE_PAGE_TOP_LEFT, ENHANCE_PAGE_BOT_RIGHT)

rect_dict = {
    "enhance equipment": ENHANCE_PAGE_RECT,
    "equipped by": EQUIPPED_BY_RECT,
    "substat text": SUBSTAT_TEXT_RECT,
    "substat roll": SUBSTAT_ROLL_RECT,
    "gear level": GEAR_LEVEL_RECT,
    "gear enhance": GEAR_ENHANCE_RECT,
    "gear type": GEAR_TYPE_RECT
}

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (102,255,0)
ORANGE_MIN = (5, 100, 50)
ORANGE_MAX = (15, 255, 255)

RECT_BORDER_SIZE = 2


def make_rectangle_around(image, boundary):
    image_with_rect = cv2.rectangle(image, rect_dict[boundary][0], rect_dict[boundary][1], WHITE, RECT_BORDER_SIZE)
    return image_with_rect


def crop_image_around(image, boundary):
    rectangle_to_crop = rect_dict[boundary]

    top_left = rectangle_to_crop[0]
    bot_right = rectangle_to_crop[1]

    top = top_left[1]
    left = top_left[0]
    bot = bot_right[1]
    right = bot_right[0]

    return image[top:bot, left:right]

def filter_orange_from_image(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    orange_mask = cv2.inRange(image_hsv, ORANGE_MIN, ORANGE_MAX)
    invert_orange_mask = cv2.bitwise_not(orange_mask) # maybe could be replaced with 255 - orange_mask

    return cv2.bitwise_and(image, image, mask=invert_orange_mask)

def transform_image_bw(image, threshold):
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, image_bw) = cv2.threshold(image_grayscale, threshold, 255, cv2.THRESH_BINARY_INV)
    return image_bw

def upscale_image(image, scale):
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
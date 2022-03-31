from random import random, uniform, randrange
import sys
import cv2
import mss
import time
import numpy as np
import pyautogui
from appscript import app, k

try:
    from pyclick import HumanClicker
except ImportError or ModuleNotFoundError:
    print('pyclick not found! Run pip install -r requirements.txt again.')
    time.sleep(5)
    sys.exit(1)

hc = HumanClicker()
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.MINIMUM_SLEEP = 0.1
pyautogui.PAUSE = 1


def moveDestination(x, y, time=2):
    if (sys.platform == "darwin"):
        hc.move((int(x/2), int(y/2)), time)
    else:
        hc.move((int(x), int(y)), time)


def clickDestination(x, y, duration=2):
    moveDestination(x, y, duration)
    time.sleep(1)
    pyautogui.click()


def clickDestinationImage(img, name=None, timeout=2, threshold=0.7):
    if not name is None:
        pass

    start = time.time()
    while(True):
        matches = getImagePositions(img, threshold)
        if(len(matches) == 0):
            has_timed_out = time.time()-start > timeout
            if(has_timed_out):
                return False

            continue

        x, y, w, h = matches[0]

        pos_click_x = round(x+w/2+uniform(2, 10))
        pos_click_y = round(y+h/2+uniform(-2, -10))

        clickDestination(pos_click_x, pos_click_y, 2)

        #pyautogui.moveTo(pos_click_x, pos_click_y, 1 + random()/2)
        # pyautogui.click()

        return True

def scroll(y, step = 1):
    # if (y < 0):
    #     y = -y
    #     step = -step
    # for s in range(y):
    #     sl = randrange(3,6,1)
    #     mouse.scroll(0, step)
    #     time.sleep(sl * 0.01)
    pyautogui.scroll(y)

def scrollDrag(x, y, duration=1):
    pyautogui.dragRel(0, y, duration, button='left')

def closeLunaTab():
    app('System Events').keystroke('w', using=k.command_down)
    print("Close Luna Tab")


def hasImage(name, threshold=0.7, img=None):
    image = getImagePositions(name, threshold, img)

    return len(image) > 0


def getImage(filename):
    path = 'target_images/' + filename

    return cv2.imread(path)


def getImagePositions(imageName, threshold=0.7, img=None):
    if img is None:
        img = printSreen()

    target = getImage(imageName)

    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    return rectangles


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))

        return sct_img[:, :, :3]


def handlePopup(screen=None):
    time.sleep(1)
    if screen is None:
        screen = printSreen()
    
    if(hasImage('button-ok.png', 0.8, screen)):
        clickDestinationImage('button-ok.png', None, 2, 0.8)

    if(hasImage('button-x.png', 0.8, screen)):
        clickDestinationImage('button-x.png', None, 2, 0.8)

def refreshTab():
    if (sys.platform == "darwin"):
        app('System Events').keystroke('r', using=k.command_down)
    else:
        pyautogui.hotkey('ctrl', 'f5')
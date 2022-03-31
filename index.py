# -*- coding: utf-8 -*-
from cv2 import cv2
from mss import ScreenShotError
from os import listdir, system
from random import randint, uniform
from random import random

import numpy as np
import pyautogui
import sys
import time
from src import login, helper, bosshunt, heroselect, fight, date
from appscript import app, k

try:
    import pygetwindow
except NotImplementedError or ModuleNotFoundError:
    print('pygetwindow not suported')


#pyautogui.PAUSE = pause
pyautogui.FAILSAFE = False

wolf = """
                                                                  .
                                                                 / V\\
                                                               / `  /
                                                              <<   |
                                                              /    |
                                                            /      |
                                                          /        |
                                                        /    \  \ /
                                                       (      ) | |
                                               ________|   _/_  | |
                                             <__________\______)\__)
=========================================================================
======================== LUS BUSD BNB USDT USDC =========================
============== 0xa24d8b3637e112489B0C956eEe2Cd8bEc826d6FF ===============
=========================================================================
============== https://github.com/walterdis/lunarush-bot ================
=========================================================================
============== MAKE SURE YOU HAVE THESE SETTINS =========================
=========================================================================
= GAME QUALITY: MEDIUM ==================================================
= BROWSER ZOOM: 100% ====================================================
= LANGUAGE: ENGLISH =====================================================
=========================================================================
============================ PLEASE DONATE ;( ===========================
=========================================================================
"""


# print(wolf)
multiaccount = false

def main():
    time.sleep(1)

    args = sys.argv[1:]
    if len(args) == 1 and args[0] == 'multi':
        multiaccount = true

    if (sys.platform == "darwin"):
        while True:
            try:
                playmacOS()
                
            except ScreenShotError:
                print('ScreenShot Error! Trying again...')
                helper.moveDestination(0,0)
            except RuntimeError:
                print('Runtime Error! Trying again...')
    
    if(sys.platform == "linux" or sys.platform == "linux2"):
        while True:
            play()

            # 3600 seconds = 1 hour
            waitTime = 9600 + uniform(20, 300)
            print('Waiting ', round(waitTime), ' seconds...')
            time.sleep(waitTime)

    gameScreens = pygetwindow.getWindowsWithTitle('Luna Rush')
    print('Windows with "Luna Rush" text title found: ', len(gameScreens))

    while True:
        for current in gameScreens:
            if "token" in current.title.lower():
                continue

            try:
                current.activate()
                if not current.isMaximized:
                    print('not maximized')
                    current.maximize()
            except:
                current.minimize()
                current.maximize()

            play()

            time.sleep(2)

        waitTime = 5000 + uniform(20, 300)
        print('Finished all plays... waiting ', round(waitTime), ' seconds to begin again.')
        time.sleep(waitTime)

def playmacOS():
    if (multiaccount):
        chrome = "open -a /Applications/Google\ Chrome.app https://app.lunarush.io"
        brave = "open -a /Applications/Brave\ Browser.app https://app.lunarush.io"

        for current in ['Google Chrome', 'Brave Browser']:
            try:
                app(current).activate()
                if current == 'Google Chrome':
                    system(chrome)
                else:
                    system(brave)
            except:
                app(current).activate()
    
            play()
            helper.closeLunaTab()
    
            time.sleep(2)
    
        print('Finished all plays... waiting to begin again.')
        time.sleep(9500+uniform(20, 300))
    
    else:
        play()
        time.sleep(10000+uniform(300, 600))


def play():
    while True:
        helper.handlePopup()

        now = time.time()

        screen = helper.printSreen()
        if(isLoginScreen(screen)):
            print('Login screen found!!!')
            login.doLogin()
            screen = helper.printSreen()
            
        if(isModeSelectScreen(screen)):
            print('Mode select found!!!')
            helper.clickDestinationImage(
                'boss-fight-mode-icon.png', 'boss-fight-mode')
            time.sleep(2)
            screen = helper.printSreen()

        if(isBossHuntStageSelect(screen)):
            print('Boss stage select screen found!!!')
            bosshunt.execute()
            time.sleep(2)
            screen = helper.printSreen()

        if(isHeroSelectScreen(screen)):
            print('Hero select screen found!!!')
            hasHero = heroselect.execute(screen)

            if(not hasHero):
                break
            screen = helper.printSreen()

        fight.execute(screen)

        print('waiting ...')
        time.sleep(1)


def isLoginScreen(screen):
    positions = helper.getImagePositions('connect-wallet.png', 0.7, screen)

    return len(positions) > 0


def isModeSelectScreen(screen):
    positions = helper.getImagePositions(
        'boss-fight-mode-icon.png', 0.7, screen)

    return len(positions) > 0


def isModeSelectScreen(screen):
    positions = helper.getImagePositions(
        'boss-fight-mode-icon.png', 0.7, screen)

    return len(positions) > 0


def isBossHuntStageSelect(screen):
    positions = helper.getImagePositions('boss-hunt-map.png', 0.7, screen)

    return len(positions) > 0


def isHeroSelectScreen(screen):
    positions = helper.getImagePositions('boss-hunt-button.png', 0.7, screen)

    return len(positions) > 0


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    print('Program exited with Ctrl+C')

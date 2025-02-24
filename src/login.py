
import pyautogui
from src.helper import clickDestinationImage
from appscript import app, k

login_attempts = 0


def doLogin():
    global login_attempts

    if login_attempts > 3:
        print('>>> Too many login attempts, refreshing')

        login_attempts = 0
        app('System Events').keystroke('r', using=k.command_down)

        return

    if clickDestinationImage('connect-wallet.png', name='connect-wallet-btn', timeout=12):
        print('Logging in!')

        login_attempts = login_attempts + 1

    if clickDestinationImage('wallet-sign.png', name='sign button', timeout=12):
        login_attempts = login_attempts + 1

        if clickDestinationImage('boss-fight-mode-icon.png', name='Boss Hunt', timeout=15):
            login_attempts = 0

        return

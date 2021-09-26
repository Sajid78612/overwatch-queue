import time
import keyboard
import pyautogui
from pyautogui import *
from win32gui import GetWindowText, GetForegroundWindow
from PIL import Image
from pytesseract import *
import requests

pytesseract.tesseract_cmd = r'C:\Users\Sajid\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
game_status = "SEARCHING"
counter = 0
header = {
    "authorization": "ENTER_KEY_HERE"
}
while True:
    if keyboard.is_pressed('ctrl+l') and GetWindowText(GetForegroundWindow()) == "Overwatch":
        while game_status == "SEARCHING":
            while not GetWindowText(GetForegroundWindow()) == "Overwatch":
                time.sleep(5)
            start_time = time.time()
            screenshot1 = pyautogui.screenshot(region=(810, 50, 300, 100))
            screenshot1.save(r"F:\overwatch-queue\img1.png")
            img1 = Image.open("img1.png")
            output1 = pytesseract.image_to_string(img1)

            if "TIME ELAPSED" in output1:
                if counter == 0:
                    payload = {
                        "content": """---------------------------
@here SEARCHING FOR GAME"""
                    }
                    r = requests.post("https://discord.com/api/v9/channels/891637820714799165/messages",
                                      data=payload,
                                      headers=header)
                game_status = "SEARCHING"
                print("SEARCHING FOR A GAME")
                counter += 1

            elif "GAME FOUND" in output1:
                print("GAME FOUND")
                payload = {
                    "content": """@here GAME FOUND"""
                }
                r = requests.post("https://discord.com/api/v9/channels/891637820714799165/messages",
                                  data=payload,
                                  headers=header)
                counter = 0
                break
            else:
                end_time = time.time()
                time_elapsed = (end_time - start_time)
                if (end_time - start_time) >= 300:
                    break
            time.sleep(0.1)

# https://discord.com/api/v9/channels/891637820714799165/messages

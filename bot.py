import time
import keyboard
import pyautogui
from pyautogui import *
import win32gui
from win32gui import GetWindowText, GetForegroundWindow
from PIL import Image
import pytesseract
from pytesseract import *
import requests
import tkinter as tk
from tkinter import filedialog, Text
import os
import threading as tr
import discord
import asyncio


async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def take_screenshot(screensize):
    if screensize == "1920x1080":
        screenshot1 = pyautogui.screenshot(region=(810, 50, 300, 100))
        screenshot1.save("images/img1.png")
    elif screensize == "2560x1440":
        screenshot1 = pyautogui.screenshot(region=(1100, 60, 380, 130))
        screenshot1.save("images/img1.png")


def screen_size():
    screenshot_sizer = pyautogui.screenshot()
    return str(screenshot_sizer.size[0]) + "x" + str(screenshot_sizer.size[1])


def discord_notify(payload, header):
    r = requests.post("https://discord.com/api/v9/channels/891637820714799165/messages",
                      data=payload,
                      headers=header)
    print(r)
    print(header)


def get_auth_discord():
    # with open("discord_token.txt", "r") as auth:
    #     token = auth.readlines()
    # return token[0]
    return "ENTER_TOKEN_HERE"


# Variables
global running_thread
global running
running = False
client = discord.Client()
channel = client.get_channel(891637820714799165)
ow_hwnd = win32gui.FindWindow(None, 'Overwatch')
resolution = screen_size()
os.environ["TESSDATA_PREFIX"] = "tesseract/tessdata"
pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
game_status = "SEARCHING"
counter = 0
# Enter your discord authorization token (google to find out how)
header = {
    "authorization": "Bot " + get_auth_discord()
}

#############GUI#############

root = tk.Tk()
root.title("OW Queue Notifier")

frame1 = tk.Frame(root, width=200, bg="#263d42", padx=5, pady=5)
frame1.pack(fill=tk.BOTH, expand=True)

frame2 = tk.Frame(root, width=50, bg="#263d42", padx=5, pady=5)
frame2.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(
    master=frame1,
    text="Overwatch Queue Tool",
    fg="orange",
    bg="#263d42",
    width=20,
    height=5
)
lbl_title.pack()

start_btn = tk.Button(
    frame2,
    text="Start",
    padx=10,
    pady=5,
    fg="white",
    bg="#263d42"
)
start_btn.pack()

lbl_primary_alert = tk.Label(
    master=frame2,
    fg="red",
    bg="#263d42",
    width=25
)
lbl_primary_alert.pack(side=tk.BOTTOM)

lbl_secondary_alert = tk.Label(
    master=frame2,
    fg="green",
    bg="#263d42",
    width=25
)
lbl_secondary_alert.pack(side=tk.BOTTOM)


# Main Loop
def start_search():
    counter = 0
    lbl_secondary_alert['text'] = ""
    if not ow_hwnd:
        lbl_primary_alert['text'] = "Overwatch not found"
    else:
        lbl_primary_alert['text'] = ""
        start_btn['text'] = "Waiting for search"
        start_btn['fg'] = "blue"
        start_btn['bg'] = "white"

        win32gui.SetForegroundWindow(ow_hwnd)
        time.sleep(2)
        # if keyboard.is_pressed('ctrl+l') and GetWindowText(GetForegroundWindow()) == "Overwatch":
        while True:
            if win32gui.GetForegroundWindow() == ow_hwnd:
                start_time = time.time()
                take_screenshot(resolution)
                img1 = Image.open("images/img1.png")
                output1 = pytesseract.image_to_string(img1)

                if "SEARCHING" in output1:
                    start_btn['text'] = "Searching for a game"
                    start_btn['fg'] = "white"
                    start_btn['bg'] = "green"
                    if counter == 0:
                        payload = {
                            "content": """---------------------------
@here SEARCHING FOR GAME"""
                        }
                        discord_notify(payload, header)
                        # channel.send(payload)
                    counter += 1

                elif "GAME FOUND" in output1:
                    start_btn['text'] = "Game Found!"
                    start_btn['fg'] = "red"
                    start_btn['bg'] = "white"
                    payload = {
                        "content": """@here GAME FOUND"""
                    }
                    discord_notify(payload, header)
                    # payload = """@here GAME FOUND"""
                    # channel.send(payload)
                    break


def start(event):
    global running, running_thread
    if not running:
        running_thread = tr.Thread(target=start_search, daemon=True)
        running_thread.start()
        running = True
    if running and not running_thread.is_alive():
        start_btn['text'] = "Start"
        start_btn['fg'] = "blue"
        start_btn['bg'] = "white"
        running = False


start_btn.bind("<Button-1>", start)


# https://discord.com/api/v9/channels/891637820714799165/messages


async def open_window():
    await client.wait_until_ready()
    channel = client.get_channel(891637820714799165)
    root.mainloop()


if __name__ == '__main__':
    client.loop.create_task(open_window())
    client.run(get_auth_discord())

import os
import pyautogui
from time import sleep
import easyocr
from ahk import AHK
sleep(5)
ahk = AHK()
os.chdir('png')
while True:
    try:
        flag = 0
        main = ahk.pixel_get_color(10,30)
        x, y = pyautogui.locateCenterOnScreen("main_bet.png")
        ahk.click(x, y)
        ahk.double_click()
        while ahk.pixel_get_color(10,30) == main:
            sleep(0.3)
            ahk.click()
        sleep(1)
        cof_list = {}
        item = 340
        reader = easyocr.Reader(["en"])
        for i in range(0, 6):
            # pyautogui.moveTo(160, item)
            pyautogui.screenshot(imageFilename=rf"C:\Users\Andrey Danilov\PycharmProjects\bot_gta_online\png\{i}.png",
                                  region=(173, item, 100, 50))
            text = reader.readtext(rf"C:\Users\Andrey Danilov\PycharmProjects\bot_gta_online\png\{i}.png", detail=0)
            ch = int(text[0].replace('/', ''))
            if ch in cof_list.values() and ch == 11:
                flag = 1
            cof_list[f'{i}.png'] = ch

            item += 121
        sor = sorted(cof_list.items(), key=lambda x: x[1])
        sor = dict(sor)
        firs_hours = list(sor.keys())[0]
        now = ahk.pixel_get_color(1160, 280)
        x, y = pyautogui.locateCenterOnScreen(firs_hours)
        ahk.click(x, y)
        ahk.double_click()
        while ahk.pixel_get_color(1160, 280) == now:
            ahk.click()
        sleep(0.7)
        if flag != 1:
            ahk.key_press('tab')
            sleep(0.7)
        x, y = pyautogui.locateCenterOnScreen('place_bet_befor_run.png')
        ahk.click(x, y)
        ahk.double_click()
        now = ahk.pixel_get_color(1160, 280)
        while ahk.pixel_get_color(1160, 280) == now:
            ahk.click()
        while pyautogui.locateCenterOnScreen('put_it_again.png') == None:
            sleep(1)
        else:
            now = ahk.pixel_get_color(10, 30)
            x, y = pyautogui.locateCenterOnScreen('put_it_again.png')
            ahk.click(x, y)
            ahk.double_click()
            sleep(1)
            while ahk.pixel_get_color(10, 30) == now:
                ahk.click(x, y)
                ahk.double_click()
                sleep(1)
    except:
        print("Программа остановлена")
        break
# print(dict(sor)
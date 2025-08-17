import pyautogui
import time
from playsound import playsound

#Miscrit you are looking for
miscrit = 'PERFECT.png'
#Which location to click to search for miscrit 961 516 Bflower
LOCATION_TO_FIND = (959,519)

battle = 'realBattle.png'

def click(x, y):
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown()
    time.sleep(0.03)
    pyautogui.mouseUp()

def check():
    try:
        location = pyautogui.locateOnScreen(miscrit, region=(1126,63, 40, 40), grayscale=True, confidence=0.55)
        if location:
            return True
        else:
            return False
    except pyautogui.ImageNotFoundException:
        return False

def inBattle():
    try:
        location = pyautogui.locateOnScreen(battle, region=(635,987, 140, 60), grayscale=True, confidence=0.4)
        if location:
            return True
        else:
            return False
    except pyautogui.ImageNotFoundException:
        return False

def doBattle():
    click(722,1022)
    time.sleep(10)
    

file = open("count.txt","r")
count = int(file.readline())
file.close()

time.sleep(5)
while True:
    count = count+1
    print(count)
    file = open("count.txt","w")
    file.write(str(count))
    file.close()
    click(LOCATION_TO_FIND[0],LOCATION_TO_FIND[1])
    time.sleep(7)
    if check():
        print("FOUND!")
        playsound('sound.mp3')
        while True:
            click(884,1015)
            time.sleep(10)
        break
    if inBattle():
        while(inBattle()):
            if check():
                print("FOUND!")
                playsound('sound.mp3')
                while True:
                    click(884,1015)
                    time.sleep(10)
                break            
            doBattle()
        click(955,798)
        time.sleep(5)
    else:
        time.sleep(15)






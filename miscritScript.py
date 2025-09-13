import pyautogui
import time
import pytesseract
from rapidfuzz import fuzz
import pygame


#Bonus
BONUS = False
BONUS_LOCATION = (705,750)

#Miscrit name you are looking for in lower case
MISCRIT = "papa"

#Which location to click to search for miscrit
LOCATION_TO_FIND = (653, 239)

CAPTURE_RATE = (644,206,55,22)

CAPTURE_LOCATION = (673, 192)

ACCEPT_CAPTURE = (608,576)

MISCRIT_NAME_LOCATION = (935, 97, 105, 13)

CONTINUE_AFTER_BATTLE = (675, 685)

BATTLE_ABILITY_NAME = "bastion"
BATTLE_ABILITY_LOCATION = (540, 730, 100, 25)
SAFE_ABILITY_LOCATION = (550, 735)

ABILITY_TO_USE_LOCATION = (345,735)

LEVEL_UP_BOTTOM_LEFT = (370, 460, 100, 14)
LEVEL_UP_TOP_RIGHT = (540, 350, 100, 14)
LEVEL_UP_BOTTOM_RIGHT = (540, 460, 100, 14)
LEVEL_CHECKER = [LEVEL_UP_BOTTOM_RIGHT,LEVEL_UP_BOTTOM_LEFT, LEVEL_UP_TOP_RIGHT]
READY_TO_TRAIN = "ready to train"


TRAIN_LOCATION = (593, 109)
FIRST_MISCRIT_TO_TRAIN = (405, 250)
SECOND_MISCRIT_TO_TRAIN = (405, 300)
THIRD_MISCRIT_TO_TRAIN = (405, 350)

MISCRITS_TO_BE_TRAINED = [FIRST_MISCRIT_TO_TRAIN, SECOND_MISCRIT_TO_TRAIN, THIRD_MISCRIT_TO_TRAIN]

EVOLUTION_CLOSE = (668,693)

TRAIN_NOW_BUTTON_LOCATION = (710, 160)
TRAIN_CONTINUE = (809, 734)
NEW_SKILL_CONTINUE = (803, 569)
EXIT_TRAIN = (1030, 130)


def click(x, y):
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown()
    time.sleep(0.03)
    pyautogui.mouseUp()

def checker(region, comparator):
    screenshot = pyautogui.screenshot(region=region)

    obtained_string = pytesseract.image_to_string(screenshot, config='--psm 6').strip().lower()

    if (comparator == MISCRIT):
        print("miscrit: "+obtained_string)
        print("fuzz: "+str(fuzz.ratio(obtained_string, comparator)))
        file = open("log.txt","a")
        file.write("\n"+obtained_string)
        file.close()
        if (obtained_string==""):
            result = percentage_parser()
            if (result < 5 and result > 0):
                return True
            return False

    
    if (fuzz.ratio(obtained_string, comparator)>70):
        return True
    else:
        return False

def grade_checker():
    result = percentage_parser()
    if (result <= 0):
        return False
    if (result <= 31):
        print("res: "+str(result))
        return True
    return False

def capture_checker():
    result = percentage_parser()
    if (result >= 65):
        return True
    if (result == 0):
        return True
    return False

def percentage_parser():
    screenshot = pyautogui.screenshot(region=CAPTURE_RATE)
    obtained_percentage = pytesseract.image_to_string(screenshot, config='--psm 7').strip()

    try:
        return string_to_int(obtained_percentage)
    except:
        return -1


def string_to_int(string):
    remove_percentage = string[:-1]
    return int(remove_percentage)    

def do_battle():
    click(ABILITY_TO_USE_LOCATION[0], ABILITY_TO_USE_LOCATION[1])
    time.sleep(8)
    
def check_all_level_up_ready(level_checker):
    for location in level_checker:
        if not checker(location, READY_TO_TRAIN):
            return False
    return True

def perform_level_up():
    click(TRAIN_LOCATION[0], TRAIN_LOCATION[1])
    time.sleep(2)

    for i in MISCRITS_TO_BE_TRAINED:
        click(i[0], i[1])
        time.sleep(1)

        click(TRAIN_NOW_BUTTON_LOCATION[0], TRAIN_NOW_BUTTON_LOCATION[1])
        time.sleep(2)

        click(BONUS_LOCATION[0], BONUS_LOCATION[1])
        click(BONUS_LOCATION[0], BONUS_LOCATION[1])
        time.sleep(3)
        click(BONUS_LOCATION[0], BONUS_LOCATION[1])
        time.sleep(5)

        click(NEW_SKILL_CONTINUE[0], NEW_SKILL_CONTINUE[1])
        time.sleep(4)

        try:
            evolution = pyautogui.locateOnScreen('/home/vboxuser/Desktop/MiscritsScript/evolution.png', confidence=0.7, grayscale=True)
            if(evolution):
                print("close evolution")
                click(EVOLUTION_CLOSE[0], EVOLUTION_CLOSE[1])
                time.sleep(2)
            else:
                print("no evolution")
        except:
            print("no evolution")
    
    click(EXIT_TRAIN[0], EXIT_TRAIN[1])
    time.sleep(3)


def main():
    file = open("count.txt","r")
    count = int(file.readline())
    file.close()

    time.sleep(5)
    while True:
        all_ready = False

        count = count+1
        print(count)
        file = open("count.txt","w")
        file.write(str(count))
        file.close()

        click(LOCATION_TO_FIND[0],LOCATION_TO_FIND[1])
        time.sleep(7)
        to_catch = False
        if checker(BATTLE_ABILITY_LOCATION, BATTLE_ABILITY_NAME):
            while(checker(BATTLE_ABILITY_LOCATION, BATTLE_ABILITY_NAME)):
                if to_catch or grade_checker():
                      to_catch = True
                      if capture_checker():
                          #capture logic
                          click(CAPTURE_LOCATION[0], CAPTURE_LOCATION[1])
                          time.sleep(10)
                          #click capture
                          #click yes
                          click(ACCEPT_CAPTURE[0], ACCEPT_CAPTURE[1])
                if checker(MISCRIT_NAME_LOCATION, MISCRIT):
                    print("FOUND!")
                    pygame.mixer.init()
                    pygame.mixer.music.load("/home/vboxuser/Desktop/MiscritsScript/sound.mp3")
                    pygame.mixer.music.play()
                    time.sleep(2)
                    while True:
                        click(SAFE_ABILITY_LOCATION[0], SAFE_ABILITY_LOCATION[1])
                        time.sleep(10)   
                    
                do_battle()
            
            time.sleep(5)
            all_ready = check_all_level_up_ready(LEVEL_CHECKER)
            click(CONTINUE_AFTER_BATTLE[0] ,CONTINUE_AFTER_BATTLE[1])
            time.sleep(5)

            if(all_ready):
                perform_level_up()
            
            if_close = True
            while if_close:
                try:
                    close_location = pyautogui.locateOnScreen('/home/vboxuser/Desktop/MiscritsScript/close.png', confidence=0.75, grayscale=True)
                    if(close_location):
                        print("need closing")
                        pyautogui.click(close_location)
                        time.sleep(3)
                    else:
                        if_close = False
                except:
                    if_close = False


        else:
            time.sleep(20)

main()
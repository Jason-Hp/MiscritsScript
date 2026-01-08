import pyautogui
import time
import pytesseract
from rapidfuzz import fuzz
import pygame
from location import Location
from coordinates import Coordinates
from kafka_producer import Action, MiscritInfo, MiscritsKafkaProducer

#*UPDATE* Miscrit name you are looking for in lower case
MISCRIT = "papa"

#*UPDATE* Miscrit (x, y) location
LOCATION_TO_FIND = (653, 239)

#*UPDATE* Ability name
BATTLE_ABILITY_NAME = "bastion"

READY_TO_TRAIN = "ready to train"

# Level checker coordinates
LEVEL_CHECKER = [Coordinates.LEVEL_UP_BOTTOM_RIGHT.value, Coordinates.LEVEL_UP_BOTTOM_LEFT.value, Coordinates.LEVEL_UP_TOP_RIGHT.value]

# Miscrits to be trained
MISCRITS_TO_BE_TRAINED = [Location.FIRST_MISCRIT_TO_TRAIN.value, Location.SECOND_MISCRIT_TO_TRAIN.value, Location.THIRD_MISCRIT_TO_TRAIN.value]

kafka_producer = MiscritsKafkaProducer()

def click(x, y):
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown()
    time.sleep(0.03)
    pyautogui.mouseUp()


def click_point(point):
    x, y = point
    click(x, y)

def get_miscrit_name(region):
    screenshot = pyautogui.screenshot(region=region)

    obtained_string = pytesseract.image_to_string(screenshot, config='--psm 6').strip().lower()

    return obtained_string

def checker(region, comparator):

    obtained_string = get_miscrit_name(region)

    if (comparator == MISCRIT):
        print("miscrit: "+obtained_string)
        print("fuzz: "+str(fuzz.ratio(obtained_string, comparator)))
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
    screenshot = pyautogui.screenshot(region=Coordinates.CAPTURE_RATE.value)
    obtained_percentage = pytesseract.image_to_string(screenshot, config='--psm 7').strip()

    try:
        return string_to_int(obtained_percentage)
    except:
        return -1


def string_to_int(string):
    remove_percentage = string[:-1]
    return int(remove_percentage)    

def do_battle():
    click_point(Location.ABILITY_TO_USE_LOCATION.value)
    time.sleep(8)
    
def check_all_level_up_ready(level_checker):
    for location in level_checker:
        if not checker(location, READY_TO_TRAIN):
            return False
    return True

def perform_level_up():
    click_point(Location.TRAIN_LOCATION.value)
    time.sleep(2)

    for i in MISCRITS_TO_BE_TRAINED:
        click_point(i)
        time.sleep(1)

        click_point(Location.TRAIN_NOW_BUTTON_LOCATION.value)
        time.sleep(2)

        click_point(Location.BONUS_LOCATION.value)
        click_point(Location.BONUS_LOCATION.value)
        time.sleep(3)
        click_point(Location.BONUS_LOCATION.value)
        time.sleep(5)

        click_point(Location.NEW_SKILL_CONTINUE.value)
        time.sleep(4)

        try:
            evolution = pyautogui.locateOnScreen('/home/vboxuser/Desktop/MiscritsScript/evolution.png', confidence=0.7, grayscale=True)
            if(evolution):
                print("close evolution")
                click_point(Location.EVOLUTION_CLOSE.value)
                time.sleep(2)
            else:
                print("no evolution")
        except:
            print("no evolution")
    
    click_point(Location.EXIT_TRAIN.value)
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

        click_point(LOCATION_TO_FIND)
        time.sleep(7)
        to_catch = False
        if checker(Coordinates.BATTLE_ABILITY_LOCATION.value, BATTLE_ABILITY_NAME):
            find_action = Action(id=count, is_successful=True, description="Successfully found and is battling a miscrit", name="find")
            kafka_producer.send_action(find_action, key="find")
            produced_miscrit_info_message = False
            while(checker(Coordinates.BATTLE_ABILITY_LOCATION.value, BATTLE_ABILITY_NAME)):

                if not produced_miscrit_info_message:
                    miscrit_info = MiscritInfo(miscrit_name=get_miscrit_name(Coordinates.MISCRIT_NAME_LOCATION.value), is_high_grade_or_rare=grade_checker(), initial_capture_rate=percentage_parser())
                    kafka_producer.send_miscrit_info(miscrit_info)
                    produced_miscrit_info_message = True

                if checker(Coordinates.MISCRIT_NAME_LOCATION.value, MISCRIT):
                    print("FOUND!")
                    time.sleep(2)
                    while True:
                        click_point(Location.SAFE_ABILITY_LOCATION.value)
                        time.sleep(10)

                if to_catch or grade_checker():
                      to_catch = True
                      if capture_checker():
                          capture_action = Action(id=count, is_successful=True, description=get_miscrit_name(Coordinates.MISCRIT_NAME_LOCATION.value), name="capture")
                          kafka_producer.send_action(capture_action, key="capture")
                          #capture logic
                          click_point(Location.CAPTURE_LOCATION.value)
                          time.sleep(10)
                          #click capture
                          #click yes
                          click_point(Location.ACCEPT_CAPTURE.value)

                do_battle()

            time.sleep(5)
            all_ready = check_all_level_up_ready(LEVEL_CHECKER)
            click_point(Location.CONTINUE_AFTER_BATTLE.value)
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

if __name__ == "__main__":
    main()

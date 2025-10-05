import pyautogui
import time
import pytesseract
from rapidfuzz import fuzz
import pygame
try:
    import pygetwindow as gw  # For window size/position
except ImportError:
    gw = None


# Config: coordinate mode
# If True, use percentage-based coordinates relative to the game window
# If False, use absolute pixel coordinates (existing behavior)
USE_RELATIVE_COORDS = False

# Window selection: set a part of the window title to match (case-insensitive)
# Example: "Miscrits" or the browser tab title where the game runs.
# If empty or no match found, active/foreground window will be used.
WINDOW_TITLE_SUBSTRING = ""

# Internal cache for window bounds (left, top, width, height)
WINDOW_BOUNDS = None


# Bonus
BONUS = False
BONUS_LOCATION = (705,750)

#Miscrit name you are looking for in lower case
MISCRIT = "papa"

# Which location to click to search for miscrit
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


# =============================
# Relative coordinate utilities
# =============================

def _find_game_window_bounds():
    global WINDOW_BOUNDS
    # If already computed, return cached
    if WINDOW_BOUNDS is not None:
        return WINDOW_BOUNDS

    left = 0
    top = 0
    width = pyautogui.size().width
    height = pyautogui.size().height

    try:
        if gw is not None:
            win = None
            if WINDOW_TITLE_SUBSTRING:
                candidates = [w for w in gw.getAllWindows() if w.title and WINDOW_TITLE_SUBSTRING.lower() in w.title.lower() and w.isVisible]
                # Prefer active window among candidates
                active = gw.getActiveWindow()
                if active and active in candidates:
                    win = active
                elif candidates:
                    # Choose the foremost non-minimized candidate
                    visible_candidates = [w for w in candidates if not w.isMinimized]
                    win = visible_candidates[0] if visible_candidates else candidates[0]
            if win is None:
                # Fallback to active window
                active = gw.getActiveWindow()
                if active and active.isVisible:
                    win = active
            if win is not None:
                left, top, width, height = win.left, win.top, win.width, win.height
    except Exception:
        # Fall back to full screen if pygetwindow not available or errors occur
        pass

    WINDOW_BOUNDS = (left, top, width, height)
    return WINDOW_BOUNDS


def _abs_point_from_pct(point_pct):
    left, top, width, height = _find_game_window_bounds()
    px, py = point_pct
    return int(left + px * width), int(top + py * height)


def _abs_region_from_pct(region_pct):
    left, top, width, height = _find_game_window_bounds()
    rx, ry, rw, rh = region_pct
    return (
        int(left + rx * width),
        int(top + ry * height),
        int(rw * width),
        int(rh * height),
    )


def _to_abs_point(point_or_pct):
    if not USE_RELATIVE_COORDS:
        return point_or_pct
    # Treat inputs as percentages (0..1)
    return _abs_point_from_pct(point_or_pct)


def _to_abs_region(region_or_pct):
    if not USE_RELATIVE_COORDS:
        return region_or_pct
    # Treat inputs as percentages (0..1)
    return _abs_region_from_pct(region_or_pct)


def click(x, y):
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown()
    time.sleep(0.03)
    pyautogui.mouseUp()


def click_pct(point_pct):
    x, y = _to_abs_point(point_pct)
    click(x, y)

def checker(region, comparator):
    screenshot = pyautogui.screenshot(region=_to_abs_region(region))

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
    screenshot = pyautogui.screenshot(region=_to_abs_region(CAPTURE_RATE))
    obtained_percentage = pytesseract.image_to_string(screenshot, config='--psm 7').strip()

    try:
        return string_to_int(obtained_percentage)
    except:
        return -1


def string_to_int(string):
    remove_percentage = string[:-1]
    return int(remove_percentage)    

def do_battle():
    ax, ay = _to_abs_point(ABILITY_TO_USE_LOCATION)
    click(ax, ay)
    time.sleep(8)
    
def check_all_level_up_ready(level_checker):
    for location in level_checker:
        if not checker(location, READY_TO_TRAIN):
            return False
    return True

def perform_level_up():
    tx, ty = _to_abs_point(TRAIN_LOCATION)
    click(tx, ty)
    time.sleep(2)

    for i in MISCRITS_TO_BE_TRAINED:
        px, py = _to_abs_point(i)
        click(px, py)
        time.sleep(1)

        nx, ny = _to_abs_point(TRAIN_NOW_BUTTON_LOCATION)
        click(nx, ny)
        time.sleep(2)

        bx, by = _to_abs_point(BONUS_LOCATION)
        click(bx, by)
        click(bx, by)
        time.sleep(3)
        click(bx, by)
        time.sleep(5)

        cx, cy = _to_abs_point(NEW_SKILL_CONTINUE)
        click(cx, cy)
        time.sleep(4)

        try:
            evolution = pyautogui.locateOnScreen('/home/vboxuser/Desktop/MiscritsScript/evolution.png', confidence=0.7, grayscale=True)
            if(evolution):
                print("close evolution")
                ex, ey = _to_abs_point(EVOLUTION_CLOSE)
                click(ex, ey)
                time.sleep(2)
            else:
                print("no evolution")
        except:
            print("no evolution")
    
    ox, oy = _to_abs_point(EXIT_TRAIN)
    click(ox, oy)
    time.sleep(3)


def main():
    # Prime window bounds if using relative mode
    if USE_RELATIVE_COORDS:
        _find_game_window_bounds()

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

        lx, ly = _to_abs_point(LOCATION_TO_FIND)
        click(lx, ly)
        time.sleep(7)
        to_catch = False
        if checker(BATTLE_ABILITY_LOCATION, BATTLE_ABILITY_NAME):
            while(checker(BATTLE_ABILITY_LOCATION, BATTLE_ABILITY_NAME)):
                if to_catch or grade_checker():
                      to_catch = True
                      if capture_checker():
                          #capture logic
                          cx, cy = _to_abs_point(CAPTURE_LOCATION)
                          click(cx, cy)
                          time.sleep(10)
                          #click capture
                          #click yes
                          ax, ay = _to_abs_point(ACCEPT_CAPTURE)
                          click(ax, ay)
                if checker(MISCRIT_NAME_LOCATION, MISCRIT):
                    print("FOUND!")
                    pygame.mixer.init()
                    pygame.mixer.music.load("/home/vboxuser/Desktop/MiscritsScript/sound.mp3")
                    pygame.mixer.music.play()
                    time.sleep(2)
                    while True:
                        sx, sy = _to_abs_point(SAFE_ABILITY_LOCATION)
                        click(sx, sy)
                        time.sleep(10)   
                    
                do_battle()
            
            time.sleep(5)
            all_ready = check_all_level_up_ready(LEVEL_CHECKER)
            cx, cy = _to_abs_point(CONTINUE_AFTER_BATTLE)
            click(cx ,cy)
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
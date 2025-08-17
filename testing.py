import pyautogui
import time
from playsound import playsound
import pytesseract
from rapidfuzz import fuzz
import pygame

screenshot = pyautogui.screenshot(region=(740,205,110,25))
#668,693
obtained_string = pytesseract.image_to_string(screenshot, config='--psm 6').strip().lower()
print("evolution"+" : "+obtained_string+" -> "+str(fuzz.ratio(obtained_string, "evolution")))


import pyautogui
import time
from playsound import playsound
import pytesseract
from rapidfuzz import fuzz
import pygame
import mss
import mss.tools
from PIL import Image
comparator = "light ignios"
obtained_string = "light ionics"
print(fuzz.ratio(obtained_string, comparator))
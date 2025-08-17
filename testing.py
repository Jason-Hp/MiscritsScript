import pyautogui
import pytesseract
from rapidfuzz import fuzz

# No need to set tesseract_cmd path on Ubuntu if installed via apt

region1bl = (370, 460, 100, 14)
region2tr = (540, 350, 100, 14)
region3br = (540, 460, 100, 14)
regionbattle = (540, 730, 100, 25)

# Define the region to capture (left, top, width, height)
region = (938, 97, 65, 13)  # adjust based on your screen

# Take the screenshot of the defined region
screenshot = pyautogui.screenshot(region=regionbattle)

# Optional: save for debugging
# screenshot.save("debug_monster_name.png")

# Use OCR to extract the text
monster_name = pytesseract.image_to_string(screenshot, config='--psm 6').strip()

print(f"Monster Detected: {monster_name}")
#new skills 803,569

print(fuzz.ratio("ready to train"," "))
import pyautogui
import time

file = open("count.txt","r")
count = int(file.readline())
file.close()
file = open("count.txt","w")
file.write(str(count+1))
file.close()
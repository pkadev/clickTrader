import keyboard  # using module keyboard
import pyautogui
import signal
import time
import os

def write_pos_to_file(pos, file):
    with open(file, 'w') as f:
        f.write(str(pos.x) + ' ' + str(pos.y))


if os.path.isdir('settings'):
    pass
else:
    print('Settings directory does not exist')
    os.mkdir('settings')
    
 
SLEEP_TIME = 2

print ('Hold mouse over ClickTrader')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
print (pos.x)
print (pos.y)
write_pos_to_file(pos, "settings/origin")

print ('Hold mouse over buy button')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
print (pos.x)
print (pos.y)
write_pos_to_file(pos, "settings/buy")

print ('Hold mouse over sell button')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/sell")
print (pos)

print ('Hold mouse over ask')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/ask")
print (pos)

print ('Hold mouse over ask +')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/ask_inc")
print (pos)

print ('Hold mouse over bid')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/bid")
print (pos)

print ('Hold mouse over bid +')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/bid_inc")
print (pos)

print ('Hold mouse over volume')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/volume")
print (pos)

print ('Hold mouse over price')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/price")
print (pos)

print ('Hold mouse over delete all orders')
time.sleep(SLEEP_TIME)
pos = pyautogui.position()
write_pos_to_file(pos, "settings/del_order")
print (pos)
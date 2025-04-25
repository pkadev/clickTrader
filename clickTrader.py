import keyboard  # using module keyboard
import pyautogui
import signal
import traceback
import time
import datetime
import sys
import os

signal.signal(signal.SIGINT, signal.SIG_IGN)
#signal.signal(signal.SIGSTP, signal.SIG_IGN)

buy_pos = 0
sell_pos = 0
ask_pos = 0
bid_pos = 0
volume_pos = 0
price_pos = 0
position_size = 0
position_size_file = 'settings/position_size'

os.system('cls' if os.name == 'nt' else 'clear')
script_verstion = "1.3.4"
print('\nClickTrader version: ' + script_verstion, end='')
print('    (\'Shift\' + \'esc\' to exit)')  



def get_position_coordinates(pos_name):
    with open('settings/'+ pos_name, 'r') as f:
        data = f.readline()
        return pyautogui.position(data.split()[0], data.split()[1])


try:
    origin_pos = get_position_coordinates('origin')
    buy_pos = get_position_coordinates('buy')
    sell_pos = get_position_coordinates('sell')
    ask_pos = get_position_coordinates('ask')
    ask_inc_pos = get_position_coordinates('ask_inc')
    bid_pos = get_position_coordinates('bid')
    bid_inc_pos = get_position_coordinates('bid_inc')
    volume_pos = get_position_coordinates('volume')
    price_pos = get_position_coordinates('price')
    del_order_pos = get_position_coordinates('del_order')
except:
    print('No positions recorded. Run calibration.')
    sys.exit()


#BUTTON_DELAY_TIME = 0.13
BUTTON_DELAY_TIME = 0.0
ORDER_BASE_SIZE = 100
class ClickTrader:
    def __init__(self):
        self.position_size = self.read_position_size()
        self.buy_size = 0
        self.delete_order_size = 0

        self.shortKeyList = [
            ['shift', '1', self.buy_ask,      str(ORDER_BASE_SIZE * 1), 'Buy shares at ask'],
            ['shift', '2', self.buy_ask,      str(ORDER_BASE_SIZE * 2), 'Buy shares at ask'],
            ['shift', '3', self.buy_ask,      str(ORDER_BASE_SIZE * 3), 'Buy shares at ask'],
            ['shift', '4', self.buy_ask,      str(ORDER_BASE_SIZE * 4), 'Buy shares at ask'],
            ['shift', '5', self.buy_ask,      str(ORDER_BASE_SIZE * 5), 'Buy shares at ask'],
            ['shift', '6', self.buy_ask,      str(ORDER_BASE_SIZE * 6), 'Buy shares at ask'],
            ['shift', '7', self.buy_ask,      str(ORDER_BASE_SIZE * 7), 'Buy shares at ask'],
            ['shift', '8', self.buy_ask,      str(ORDER_BASE_SIZE * 8), 'Buy shares at ask'],
            ['shift', '9', self.buy_ask,      str(ORDER_BASE_SIZE * 9), 'Buy shares at ask'],
            ['shift', '0', self.buy_ask,      str(ORDER_BASE_SIZE * 10), 'Buy shares at ask'],
            ['shift', 'b', self.buy_bid,      '0', 'Buy shares at bid'],
            ['ctrl', 'z',  self.sell_bid,     '0',   'Sell whole position at bid'],
            ['ctrl', 'x',  self.sell_bid,     '0.5', 'Sell half position at bid'],
            ['ctrl', 'k',  self.sell_ask,     '0',   'Sell whole position at ask'],
            ['ctrl', 'q',  self.del_order,    '0',   'Cancel order'],
            ['ctrl', 'h',  self.print_all,    '0',   'Print all commands'],
            ['alt', 'F9',  self.set_pos_size, str(ORDER_BASE_SIZE), 'Increase internal position size'],
            ['alt', 'F11', self.dec_pos_size, str(ORDER_BASE_SIZE), 'Decrease internal position size'],
            ['alt', 'F12', self.inc_pos_size, str(ORDER_BASE_SIZE), 'Increase internal position size']
        ]

    def del_order(self, none):
        pyautogui.click(del_order_pos)
        time.sleep(0.01)
        
        pyautogui.click(origin_pos)
        self.position_size = self.delete_order_size
        print('Restored position size: ' + str(self.position_size))
        
        
    def write_position_size(self, size):
        print('New position size: ' + str(size))
        with open(position_size_file, 'w') as f:
            f.write(str(size))
   
    def read_position_size(self):
        with open(position_size_file, 'w+') as f:
            try:
                self.position_size = int(f.read())
            except:
                self.position_size = 0.0

            return self.position_size

    def buy(self, size):
        while(keyboard.is_pressed('shift')):
            pass
        pyautogui.write(size)
        pyautogui.click(buy_pos)
        #pyautogui.moveTo(buy_pos)

        self.position_size += int(size)
        self.delete_order_size = self.position_size
        self.write_position_size(self.position_size)
        pyautogui.click(origin_pos)

    def buy_ask(self, size):
        print('Buy ' + str(size) + ' shares at the ASK + 15 cents')
        pyautogui.doubleClick(ask_pos)
        self.buy(size)
       
    def buy_bid(self, size):
        print('Buy ' + str(self.buy_size) + ' shares at the BID')
        pyautogui.doubleClick(bid_pos)
        
        if self.position_size == 0:
            self.position_size = self.buy_size
            self.delete_order_size = self.position_size
        self.buy(str(self.buy_size))

    def sell(self, size):
        while(keyboard.is_pressed('shift')):
            pass
        while(keyboard.is_pressed('ctrl')):
            print ('ctrl')
            while(keyboard.is_pressed('ctrl')):
                print ('ctrl')
                pass
            print ('Let go')
        time.sleep(0.5)
        
        pyautogui.write("100")
        #pyautogui.click(sell_pos)
        pyautogui.moveTo(sell_pos)

        self.delete_order_size = self.position_size
        self.position_size -= int(size)
        self.write_position_size(self.position_size)
        #pyautogui.click(origin_pos)

    def sell_ask(self, size):
        if size == '0' and self.position_size != 0:
            size = self.position_size

        if self.position_size != 0:
            print ('Sell ask: ' + str(size))
            pyautogui.doubleClick(ask_pos)
            self.sell(size)

    def sell_bid(self, size):
        if size == '0' and self.position_size != 0:
            size = self.position_size
            print ('Get rid of whole position (' + str(size) + ')')
        elif size == '0.5' and self.position_size != 0:
            size = self.position_size / 2
            self.position_size = self.position_size - size

            print ('Sold half: ' + size)
            print ('Remaining: ' + self.position_size)
        
        
        print ('Sell bid: ' + str(size))  
        pyautogui.doubleClick(bid_inc_pos)
        self.sell(size)

    def set_pos_size(self, size):
        print('Set bid size: ')
        self.buy_size = int(input())
        
        print('Position size: ' + str(self.buy_size))

    def dec_pos_size(self, size):
        if self.position_size > 0:
            self.position_size -= int(size)
            self.delete_order_size = self.position_size

            if self.position_size < 0:
                self.position_size = 0
                
            self.write_position_size(self.position_size)

    def inc_pos_size(self, size):
        self.position_size += int(size)
        self.delete_order_size = self.position_size
        self.write_position_size(self.position_size)

    def print_all(self, none):
        for cmd in self.shortKeyList:
            print (cmd[0] + '+' + cmd[1] + ': ' + cmd[4])
       

ct = ClickTrader()

#print (ct.read_position_size())
print ('Current position size: ' + str(ct.position_size))
print ('Current position basis: ' + str(ORDER_BASE_SIZE))
###############   Program   ###############
run = True
while run:
    time.sleep(0.0001)
    try:
        for shortKey in ct.shortKeyList:    
#            print (shortKey[0] + '+' + shortKey[1] + ': ' + shortKey[2])
            if keyboard.is_pressed(shortKey[0]) and keyboard.is_pressed(shortKey[1]):
                BUTTON_DELAY_TIME = 0.2
                if shortKey[2] != None:
                    start = datetime.datetime.now()
                    shortKey[2](shortKey[3])
                    end = datetime.datetime.now()
                    interval = end - start
                    #print(interval)

                #print (shortKey[0] + '+' + shortKey[1] + ': ' + str(shortKey[2]) + ' ' + shortKey[3])
                time.sleep(BUTTON_DELAY_TIME)
            elif keyboard.is_pressed('esc') and keyboard.is_pressed('shift'):
                run = False
                break
            else:
                BUTTON_DELAY_TIME = 0.0

    except KeyboardInterrupt:
        print ('ctrl+c')
        continue
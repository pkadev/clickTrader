import keyboard  # using module keyboard
import pyautogui
import signal
import traceback
import time
import datetime

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


 

def get_position_coordinates(pos_name):
    with open('settings/'+ pos_name, 'r') as f:
        data = f.readline()
        return pyautogui.position(data.split()[0], data.split()[1])

buy_pos = get_position_coordinates('buy')
sell_pos = get_position_coordinates('sell')
ask_pos = get_position_coordinates('ask')
ask_inc_pos = get_position_coordinates('ask_inc')
bid_pos = get_position_coordinates('bid')
bid_inc_pos = get_position_coordinates('bid_inc')
volume_pos = get_position_coordinates('volume')
price_pos = get_position_coordinates('price')
del_order_pos = get_position_coordinates('del_order')

#BUTTON_DELAY_TIME = 0.13
BUTTON_DELAY_TIME = 0.0
ORDER_BASE_SIZE = 100
class ClickTrader:
    def __init__(self):
        self.position_size = self.read_position_size()

        self.shortKeyList = [
            ['shift', '1', self.buy_ask,      str(ORDER_BASE_SIZE), 'Buy shares at ask'],
            ['shift', '2', self.buy_ask,      str(ORDER_BASE_SIZE * 2), 'Buy shares at ask'],
            ['shift', 'b', self.buy_bid,      str(ORDER_BASE_SIZE), 'Buy shares at bid'],
            ['ctrl', 'z',  self.sell_bid,     '0',   'Sell whole position at bid'],
            ['ctrl', 'k',  self.sell_ask,     '0',   'Sell whole position at ask'],
            ['ctrl', 'q',  None,              '0',   'Cancel order'],
            ['ctrl', 'h',  self.print_all,    '0',   'Print all commands'],
            ['alt', 'F11', self.inc_pos_size, str(ORDER_BASE_SIZE), 'Increase internal position size'],
            ['alt', 'F12', self.dec_pos_size, str(ORDER_BASE_SIZE), 'Decrease internal position size']
        ]

    def write_position_size(self, size):
        print('New position size: ' + str(size))
        with open(position_size_file, 'w') as f:
            f.write(str(size))
   
    def read_position_size(self):
        with open(position_size_file, 'r') as f:
            self.position_size = int(f.read())
            return self.position_size

    def buy(self, size):
        pyautogui.doubleClick(volume_pos)
        pyautogui.write(size)
        pyautogui.click(buy_pos)
        #pyautogui.moveTo(buy_pos)

        #pyautogui.click(volume_pos)
        #pyautogui.write('del')
       
        pyautogui.doubleClick(volume_pos)
        pyautogui.hotkey('del')
        self.position_size += int(size)
        self.write_position_size(self.position_size)

    def buy_ask(self, size):
        print('Buy ' + str(size) + ' shares at the ASK + 15 cents')
        pyautogui.doubleClick(ask_pos)
        self.buy(size)
       
    def buy_bid(self, size):
        print('Buy ' + str(size) + ' shares at the BID - 15 cents')
        pyautogui.doubleClick(bid_pos)
        self.buy(size)

    def sell(self, size):
        pyautogui.doubleClick(volume_pos)
        pyautogui.write(str(size))
        pyautogui.click(sell_pos)
        #pyautogui.moveTo(sell_pos)

        pyautogui.doubleClick(volume_pos)
        pyautogui.hotkey('del')
        self.position_size -= int(size)
        self.write_position_size(self.position_size)

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

        print ('Sell bid: ' + str(size))  
        if int(size) >= self.position_size:
            pyautogui.doubleClick(bid_inc_pos)
            self.sell(size)
        else:
            print ('No position')

    #def sell_all(self, size):
    #    self.sell_bid(self.position_size)

    def dec_pos_size(self, size):
        if self.position_size > 0:
            self.position_size -= int(size)
            self.write_position_size(self.position_size)

    def inc_pos_size(self, size):
        self.position_size += int(size)
        self.write_position_size(self.position_size)

    def print_all(self, none):
        for cmd in self.shortKeyList:
            print (cmd[0] + '+' + cmd[1] + ': ' + cmd[4])
       

ct = ClickTrader()

#print (ct.read_position_size())
print (ct.position_size)
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
                    print(interval)

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
import time
import os, sys
import keyboard
import pyautogui

def loop():
  os.system('cls')
  print('\n -------  Mouse Auto Holder/Clicker ------- \n')
  clear = lambda: os.system('cls')

  rORl = input('Right mouse or left mouse button? (l/r) ')
  if rORl == 'l':
    rORl = 'left'
  elif rORl == 'r':
    rORl = 'right'
  else:
    print(f'The given input {rORl} is not valid.')
    time.sleep(2)
    loop()

  print('')
  for i in range(1, 6):
    print(f'Loop starting in {i}...')
    time.sleep(1)
  print("\nStarted press 'alt' to halt.")

  while True:
    if keyboard.is_pressed('win'):
      print('Windows key pressed, stalling.')
      time.sleep(5)
    if keyboard.is_pressed('alt'):
      break

    try:
      pyautogui.mouseDown(button=rORl)
    except KeyboardInterrupt:
      clear()
      print('Quitting...')
      time.sleep(2)
      sys.exit(0)
    except pyautogui.FailSafeException:
      print('\nFail safe triggered, restart?')
      quick_start = input('> ')
      if quick_start.lower() == 'yes' or 'y':
        time.sleep(2)
        continue

      else:
        clear()
        print('Quitting...')
        time.sleep(2)
        sys.exit(0)

    time.sleep(0.2)

  print("Loop halted, type 'start' to restart.")
  user_input = input('> ')
  if user_input.lower() == 'start':
    loop()
  else:
    clear()
    print('Quitting...')
    time.sleep(2)
    sys.exit(0)

if __name__ == '__main__':
  loop()
else:
  print(f'You cannot import {__file__}.')
  sys.exit(1)
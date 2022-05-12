import pyautogui

pyautogui.moveTo(100, 150)
pyautogui.click()
pyautogui.write('Hello world!', interval=0.25)
with pyautogui.hold('shift'):
  pyautogui.press(['a','b','c'])


import pyautogui

pyautogui.moveTo(100, 150)
pyautogui.click()

distance = 200
while distance > 0:
        pyautogui.drag(distance, 0, duration=0.5, button='left')   # move right
        distance -= 20
        pyautogui.drag(0, distance, duration=0.5, button='left')   # move down
        pyautogui.drag(-distance, 0, duration=0.5, button='left')  # move left
        distance -= 20
        pyautogui.drag(0, -distance, duration=0.5, button='left')  # move up

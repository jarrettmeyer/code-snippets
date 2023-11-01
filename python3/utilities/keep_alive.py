import datetime
import math
import numpy as np
import pyautogui
import time

move_mouse_interval = 120
move_mouse_duration = 1
circle_radius = 2

def move_mouse_in_circle(radius, duration):
    n_ticks = 5
    ticks = np.linspace(0, 2*math.pi, n_ticks)
    tick_interval = duration / len(ticks)

    current_x, current_y = pyautogui.position()

    for tick in ticks:
        x = current_x + radius * math.cos(tick)
        y = current_y + radius * math.sin(tick)
        pyautogui.moveTo(x, y, duration=tick_interval)
        time.sleep(tick_interval)

while True:
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'tick {now}')
    move_mouse_in_circle(circle_radius, move_mouse_duration)
    time.sleep(move_mouse_interval)


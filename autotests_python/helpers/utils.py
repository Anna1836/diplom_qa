import os
import time


def save_screenshot(driver, name="error"):
    folder = "screenshots"
    if not os.path.exists(folder):
        os.mkdir(folder)
    path = os.path.join(folder, f"screenshot_{name}_{time.time():.0f}.png")
    driver.save_screenshot(path)
    print(f"Скриншот сохранен: {path}")
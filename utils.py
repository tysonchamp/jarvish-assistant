import pyautogui
from config import SCREENSHOT_PATH

def take_screenshot(path=SCREENSHOT_PATH):
    """
    Captures the primary monitor and saves it to the specified path.
    Returns the path if successful, None otherwise.
    """
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print(f"Screenshot saved to {path}")
        return path
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return None

import pyautogui
import sys
import time
try:
    import msvcrt  # Windows-specific keyboard input
except ImportError:
    msvcrt = None

try:
    import keyboard  # Global hotkey listener
except ImportError:
    keyboard = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None


def find_window_by_title_substring(title_substring: str):
    if gw is None:
        return None
    candidates = [
        w for w in gw.getAllWindows()
        if w.title and title_substring.lower() in w.title.lower()
    ]
    if not candidates:
        return None
    active = gw.getActiveWindow()
    if active and active in candidates:
        return active
    return candidates[0]


def main():
    # Wait for user to press 'h' to start (global listener if available)
    print("Press 'h' to start the screenshot...")
    if keyboard is not None:
        keyboard.wait('h')
    elif msvcrt is not None:
        while True:
            ch = msvcrt.getwch()
            if ch.lower() == 'h':
                break
    else:
        print("keyboard/msvcrt not available; press Enter after typing 'h'.")
        while True:
            inp = input("")
            if inp.strip().lower() == 'h':
                break

    title_substring = "Miscrit"
    window = find_window_by_title_substring(title_substring)
    if window is None:
        print("Could not find a visible window with title containing 'Miscrit'.")
        if gw is None:
            print("pygetwindow is not installed; falling back to full-screen coordinates.")
        # Fallback to full screen bounds
        left, top = 0, 0
        screen_width, screen_height = pyautogui.size()
        width, height = screen_width, screen_height
    else:
        left, top, width, height = window.left, window.top, window.width, window.height

    # Percentages
    px = 0.695   # 69.5%
    py = 0.108   # 10.8%
    pw = 0.105   # 10.5%
    ph = 0.04    # 4%

    region = (
        int(left + px * width),
        int(top + py * height),
        int(pw * width),
        int(ph * height),
    )

    print(f"Window bounds: left={left}, top={top}, width={width}, height={height}")
    print(f"Capture region (x, y, w, h): {region}")

    screenshot = pyautogui.screenshot(region=region)
    output_path = "testing_capture.png"
    screenshot.save(output_path)
    print(f"Saved screenshot to {output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
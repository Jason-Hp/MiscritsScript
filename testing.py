import subprocess
import pyautogui

def get_window_geometry(window_title):
    # Run wmctrl to get the list of windows with their geometry
    result = subprocess.run(['wmctrl', '-lG'], capture_output=True, text=True)
    windows = result.stdout.splitlines()

    # Search through each window to find the one with the title
    for window in windows:
        parts = window.split()
        window_id, x, y, width, height, title = parts[0], parts[1], parts[2], parts[3], parts[4], ' '.join(parts[5:])
        
        # Check if the window title contains the substring we're looking for
        if window_title.lower() in title.lower():
            return int(x), int(y), int(width), int(height)
    
    return None

def main():
    window_title = "Miscrits"  # Adjust this title to match the window you're targeting

    # Get the window geometry using wmctrl
    geometry = get_window_geometry(window_title)
    
    if geometry is None:
        print(f"Could not find a window with title containing '{window_title}'.")
        return

    left, top, width, height = geometry
    print(f"Window geometry: left={left}, top={top}, width={width}, height={height}")

    # Define region capture percentages (adjust these to your needs)
    px, py, pw, ph = 0.478, 0.215, 0.043, 0.026

    # Calculate the capture region based on percentages
    region = (
        int(left + px * width),
        int(top + py * height),
        int(pw * width),
        int(ph * height),
    )

    # Debug: Print the calculated region for capture
    print(f"Capture region (x, y, w, h): {region}")

    # Capture the screenshot of the region
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("testing_capture.png")
    print("Screenshot saved to testing_capture.png")

if __name__ == "__main__":
    main()

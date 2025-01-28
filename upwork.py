import time
import random
from datetime import datetime
import os
import mss

def take_screenshot(save_directory):
    """Capture the screen and save it as an image file."""
    try:
        # Create an instance of mss
        with mss.mss() as sct:
            # Capture the primary monitor
            screenshot = sct.shot(mon=-1, output=os.path.join(save_directory, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"))
            print(f"Screenshot saved: {screenshot}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

def main():
    # Directory to save screenshots
    save_directory = "screenshots"
    os.makedirs(save_directory, exist_ok=True)
    
    print("Screen tracker started. Press Ctrl+C to stop.")
    try:
        while True:
            # Take a screenshot
            take_screenshot(save_directory)
            
            # Wait for a random interval (2 to 5 minutes)
            interval = random.randint(2, 5) * 60
            print(f"Next screenshot in {interval // 60} minutes.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nScreen tracker stopped.")

if __name__ == "__main__":
    main()

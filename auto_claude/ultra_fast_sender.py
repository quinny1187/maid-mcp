"""
Ultra-Fast Clipboard Sender for Claude Desktop
FIXED VERSION - Better error handling and recovery
"""

import win32gui
import win32clipboard
import win32con
import time
from pywinauto import Application
from pywinauto import findwindows
from pywinauto.keyboard import send_keys

class UltraFastClaudeSender:
    def __init__(self):
        self.app = None
        self.window = None
        self.last_check_time = 0
        self.check_interval = 5  # Re-check window every 5 seconds
    
    def find_claude_window(self, force_refresh=False):
        """Find Claude Desktop window more reliably"""
        current_time = time.time()
        
        # Use cached window if recent and not forcing refresh
        if (not force_refresh and 
            self.window is not None and 
            current_time - self.last_check_time < self.check_interval):
            try:
                # Quick check if window still valid
                if self.window.exists():
                    return self.app, self.window
            except:
                # Window no longer valid
                pass
        
        # Find Claude window
        try:
            # Method 1: Direct connection
            self.app = Application(backend="uia").connect(title="Claude", timeout=2)
            self.window = self.app.window(title="Claude")
            print("✓ Found Claude by exact title")
            self.last_check_time = current_time
            return self.app, self.window
            
        except Exception as e:
            # Method 2: Enumerate and find
            try:
                all_windows = findwindows.find_elements(class_name="Chrome_WidgetWin_1")
                
                for win in all_windows:
                    if win.name == "Claude":
                        self.app = Application(backend="uia").connect(handle=win.handle)
                        self.window = self.app.window(handle=win.handle)
                        print(f"✓ Found Claude by handle: {win.handle}")
                        self.last_check_time = current_time
                        return self.app, self.window
                
                # No Claude window found
                return None, None
                
            except Exception as e2:
                return None, None
    
    def send_message(self, message):
        """Send message with better error recovery"""
        try:
            # Remember current window
            original_window = win32gui.GetForegroundWindow()
            original_title = win32gui.GetWindowText(original_window) if original_window else "Unknown"
            
            # Find Claude window
            retry_count = 0
            while retry_count < 3:
                self.app, self.window = self.find_claude_window(force_refresh=(retry_count > 0))
                
                if self.window:
                    break
                    
                retry_count += 1
                time.sleep(0.5)
                print(f"Retry {retry_count}/3: Looking for Claude window...")
            
            if not self.window:
                raise Exception("Could not find Claude Desktop window after 3 attempts")
            
            # Try different methods to send the message
            success = False
            
            # Method 1: Set focus and use window type_keys
            try:
                self.window.set_focus()
                time.sleep(0.1)
                
                # Clear and type
                self.window.type_keys("^a", pause=0.02)
                time.sleep(0.05)
                self.window.type_keys(message, pause=0, with_spaces=True, with_tabs=True, with_newlines=True)
                time.sleep(0.05)
                self.window.type_keys("{ENTER}", pause=0)
                success = True
                
            except Exception as e1:
                print(f"Method 1 failed: {e1}")
                
                # Method 2: Use send_keys directly
                try:
                    self.window.set_focus()
                    time.sleep(0.2)
                    
                    # Use send_keys function instead of window method
                    send_keys("^a")
                    time.sleep(0.05)
                    send_keys(message)
                    time.sleep(0.05)
                    send_keys("{ENTER}")
                    success = True
                    
                except Exception as e2:
                    print(f"Method 2 failed: {e2}")
                    
                    # Method 3: Direct Win32 approach
                    try:
                        hwnd = self.window.handle
                        win32gui.SetForegroundWindow(hwnd)
                        time.sleep(0.2)
                        
                        # Select all
                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x41, 0)  # A key
                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 0x41, 0)
                        
                        # Type message using clipboard
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardText(message)
                        win32clipboard.CloseClipboard()
                        
                        # Paste
                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x56, 0)  # V key
                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 0x56, 0)
                        
                        # Enter
                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0)
                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)
                        
                        success = True
                        
                    except Exception as e3:
                        print(f"Method 3 failed: {e3}")
                        raise Exception(f"All methods failed. Last error: {e3}")
            
            if not success:
                raise Exception("Failed to send message using any method")
            
            # Return to original window
            if original_window:
                try:
                    win32gui.SetForegroundWindow(original_window)
                except:
                    pass
            
            print(f"✅ Sent! Returned to: {original_title}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nTroubleshooting:")
            print("- Make sure Claude Desktop is open and not minimized")
            print("- Try clicking on the Claude window input area")
            print("- Close and reopen Claude Desktop if needed")
            
            # Reset cached window on error
            self.window = None
            self.app = None
            
            return False

# Singleton instance
_sender_instance = None

def send_to_claude(message):
    global _sender_instance
    if _sender_instance is None:
        _sender_instance = UltraFastClaudeSender()
    return _sender_instance.send_message(message)

if __name__ == "__main__":
    print("⚡ Ultra-Fast Sender - MULTI-METHOD VERSION")
    print("-" * 40)
    
    # Test
    test_msg = "[MAID_EVENT] Test with multiple methods!"
    print(f"\nSending: {test_msg}")
    
    if send_to_claude(test_msg):
        print("✅ Success!")

"""
Simple test to verify we can find and connect to Claude Desktop
"""

from pywinauto import Application
from pywinauto import findwindows

print("🔍 Testing Claude Desktop connection...\n")

# Method 1: Direct connection
print("Method 1: Direct connection by title")
try:
    app = Application(backend="uia").connect(title="Claude", class_name="Chrome_WidgetWin_1")
    window = app.window(title="Claude", class_name="Chrome_WidgetWin_1")
    print("✅ SUCCESS! Connected to Claude Desktop")
    print(f"   Window: {window.window_text()}")
    print(f"   Class: {window.class_name()}")
    print(f"   Handle: {window.handle}")
except Exception as e:
    print(f"❌ Failed: {e}")

# Method 2: Find by enumerating
print("\n\nMethod 2: Find by enumerating windows")
try:
    all_windows = findwindows.find_elements(class_name="Chrome_WidgetWin_1")
    for win in all_windows:
        if win.name == "Claude":
            print(f"✅ Found Claude window!")
            print(f"   Title: {win.name}")
            print(f"   Handle: {win.handle}")
            print(f"   Process ID: {win.process_id}")
            
            # Try to connect
            app = Application(backend="uia").connect(handle=win.handle)
            window = app.window(handle=win.handle)
            print("✅ Successfully connected via handle!")
            break
    else:
        print("❌ No window with exact title 'Claude' found")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✨ If you see SUCCESS above, the sender should work!")
input("\nPress Enter to exit...")

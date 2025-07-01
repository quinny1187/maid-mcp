"""
Debug script to find Claude Desktop window
Helps identify the correct window among multiple matches
"""

from pywinauto import Application, findwindows
import win32gui

def list_all_windows_with_claude():
    """List all windows that might match Claude"""
    print("🔍 Searching for windows...\n")
    
    # Method 1: Using pywinauto
    print("=== PYWINAUTO SEARCH ===")
    try:
        elements = findwindows.find_elements()
        claude_matches = []
        
        for elem in elements:
            if elem.name and 'claude' in elem.name.lower():
                claude_matches.append(elem)
                
        if claude_matches:
            print(f"Found {len(claude_matches)} windows with 'Claude' in title:\n")
            for i, elem in enumerate(claude_matches):
                print(f"{i+1}. Title: {elem.name}")
                print(f"   Class: {elem.class_name}")
                print(f"   Handle: {elem.handle}")
                print(f"   Process ID: {elem.process_id}")
                print()
        else:
            print("No windows found with 'Claude' in title")
            
    except Exception as e:
        print(f"Error with pywinauto search: {e}")
    
    # Method 2: Using win32gui
    print("\n=== WIN32GUI SEARCH ===")
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text and ('claude' in window_text.lower() or 
                               'Chrome_WidgetWin' in win32gui.GetClassName(hwnd)):
                windows.append({
                    'handle': hwnd,
                    'title': window_text,
                    'class': win32gui.GetClassName(hwnd)
                })
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    # Filter for likely Claude windows
    electron_windows = [w for w in windows if w['class'] == 'Chrome_WidgetWin_1']
    
    print(f"\nFound {len(electron_windows)} Electron windows (Chrome_WidgetWin_1):")
    for i, win in enumerate(electron_windows):
        print(f"{i+1}. Title: {win['title'][:80]}{'...' if len(win['title']) > 80 else ''}")
        print(f"   Class: {win['class']}")
        print(f"   Handle: {win['handle']}")
        print()

def test_specific_patterns():
    """Test specific title patterns"""
    print("\n=== TESTING SPECIFIC PATTERNS ===")
    patterns = [
        ".*Claude.*",
        ".* - Claude$",
        "^Claude.*",
        ".*Claude Desktop.*"
    ]
    
    for pattern in patterns:
        print(f"\nTesting pattern: {pattern}")
        try:
            app = Application(backend="uia").connect(title_re=pattern)
            windows = app.windows()
            print(f"✅ Found {len(windows)} window(s)")
            for win in windows[:3]:  # Show first 3
                print(f"   - {win.window_text()[:60]}...")
        except Exception as e:
            print(f"❌ No match: {str(e)[:60]}...")

if __name__ == "__main__":
    print("🔍 Claude Desktop Window Finder Debug Tool")
    print("=" * 50)
    
    list_all_windows_with_claude()
    test_specific_patterns()
    
    print("\n💡 Tip: The Claude Desktop window usually:")
    print("- Has class name 'Chrome_WidgetWin_1' (Electron app)")
    print("- Has a long title (shows conversation content)")
    print("- Does NOT end with '.py' or other file extensions")
    
    input("\nPress Enter to exit...")

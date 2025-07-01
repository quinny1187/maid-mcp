"""
Maid-MCP Complete System Launcher
Starts all components: avatar display, state server, and voice input
"""

import subprocess
import time
import os
import sys
import signal
import psutil
from pathlib import Path

def kill_existing_processes():
    """Kill any existing maid-mcp processes"""
    print("Cleaning up existing processes...")
    
    # Process names to kill
    scripts_to_kill = [
        'avatar_display.py',
        'avatar_state_server.py', 
        'speechListener.py'
    ]
    
    killed_count = 0
    
    # Find and kill Python processes running our scripts
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = proc.info.get('cmdline', [])
                if cmdline:
                    # Check if any of our scripts are in the command line
                    for script in scripts_to_kill:
                        if any(script in arg for arg in cmdline):
                            print(f"  Killing {script} (PID: {proc.info['pid']})")
                            proc.kill()
                            killed_count += 1
                            break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Kill any process on port 3338 (avatar state server)
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == 3338 and conn.status == 'LISTEN':
                proc = psutil.Process(conn.pid)
                print(f"  Killing process on port 3338 (PID: {conn.pid})")
                proc.kill()
                killed_count += 1
    except:
        pass
    
    if killed_count > 0:
        print(f"✓ Cleaned up {killed_count} processes")
        time.sleep(2)  # Wait for processes to fully terminate
    else:
        print("✓ No existing processes found")

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"Python found: {result.stdout.strip()}")
        return True
    except:
        print("ERROR: Python not found. Please install Python 3.8+")
        return False

def start_component(name, path, script, new_window=False):
    """Start a component"""
    print(f"Starting {name}...")
    
    # Change to component directory
    original_dir = os.getcwd()
    os.chdir(path)
    
    try:
        if new_window:
            # Start in new window (for voice input)
            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', f'{name}', 'cmd', '/k', 
                                'python', script], shell=True)
            else:  # Linux/Mac
                subprocess.Popen(['gnome-terminal', '--', 'python', script])
        else:
            # Start in background
            subprocess.Popen([sys.executable, script])
        
        print(f"✓ {name} started successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to start {name}: {e}")
        return False
        
    finally:
        os.chdir(original_dir)

def main():
    """Main launcher function"""
    print("=" * 40)
    print("  Maid-MCP Complete System Launcher")
    print("=" * 40)
    print()
    
    # Kill existing processes first
    kill_existing_processes()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        return
    
    # Get base directory
    base_dir = Path(__file__).parent
    
    # Start components
    components = [
        ("Avatar Display", base_dir / "avatar", "avatar_display.py", False),
        ("Avatar State Server", base_dir / "avatar", "avatar_state_server.py", False),
        ("Voice Input Listener", base_dir / "voice" / "incoming", "speechListener.py", True)
    ]
    
    for i, (name, path, script, new_window) in enumerate(components, 1):
        print(f"\n[{i}/{len(components)}] {name}")
        
        if start_component(name, path, script, new_window):
            # Wait between starts
            if i < len(components):
                time.sleep(2)
    
    print("\n" + "=" * 40)
    print("  All systems started successfully!")
    print("=" * 40)
    print()
    print("Avatar: Running in background")
    print("Voice: Check the Voice Input window")
    print()
    print("To stop all systems:")
    print("1. Run stop_all.bat")
    print("2. Or close the Voice Input window")
    print("3. And right-click to close the avatar")
    print()
    
    try:
        input("Press Enter to stop all systems...")
        # Kill all processes on exit
        kill_existing_processes()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        kill_existing_processes()

if __name__ == "__main__":
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("ERROR: psutil module required for process management")
        print("Run: pip install psutil")
        input("Press Enter to exit...")
        sys.exit(1)
    
    main()

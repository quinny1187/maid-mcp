"""
Test script to wait for GIF mode to end before playing animations
"""
import requests
import time

def wait_for_avatar_ready(timeout=10):
    """Wait for avatar to be ready (not playing GIF)"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:3338/state")
            if response.status_code == 200:
                state = response.json()
                # Check if GIF is not playing and pose is back to idle
                if state.get('gif') is None and state.get('pose') == 'idle':
                    print("Avatar is ready!")
                    return True
        except:
            pass
        time.sleep(0.5)
    print("Timeout waiting for avatar")
    return False

if __name__ == "__main__":
    print("Waiting for avatar to be ready...")
    if wait_for_avatar_ready():
        print("Avatar ready - you can now play animations!")

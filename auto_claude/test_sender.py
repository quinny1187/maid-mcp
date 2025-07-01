"""
Quick test to verify ultra_fast_sender is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ultra_fast_sender import send_to_claude
import time

print("=" * 50)
print("  Testing Ultra Fast Sender")
print("=" * 50)
print()
print("This will send a test message to Claude Desktop")
print("Make sure Claude Desktop is open and visible!")
print()

input("Press Enter to send test message...")

print("\nSending test message...")
test_msg = "[TEST] Ultra fast sender test message!"

if send_to_claude(test_msg):
    print("\n✅ SUCCESS! Message sent to Claude!")
    print("Check if the message appeared in Claude Desktop.")
else:
    print("\n❌ FAILED! Could not send message.")
    print("\nTry:")
    print("1. Click on Claude Desktop's input area")
    print("2. Close and reopen Claude Desktop")
    print("3. Run debug_windows.py to check window detection")

input("\nPress Enter to exit...")

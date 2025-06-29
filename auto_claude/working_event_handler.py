"""
Working Event Handler with proper message spacing
Waits for Claude to respond before sending next message
"""

from ultra_fast_sender import send_to_claude
import time
import threading
import queue
from datetime import datetime

class WorkingEventHandler:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.running = False
        # Adjust this based on typical Claude response time
        self.response_wait_time = 5  # seconds to wait for Claude to respond
        
    def add_event(self, event_type, message):
        """Add event to queue"""
        self.event_queue.put({
            'type': event_type,
            'message': message,
            'time': datetime.now()
        })
        print(f"📥 Queued: {event_type} - {message}")
    
    def process_events(self):
        """Process events with proper spacing"""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                
                # Format message
                msg = f"[MAID_EVENT] {event['type']}: {event['message']}"
                
                # Send using ultra fast sender
                start = time.time()
                if send_to_claude(msg):
                    elapsed = (time.time() - start) * 1000
                    print(f"✅ Sent in {elapsed:.0f}ms: {msg}")
                else:
                    print(f"❌ Failed: {msg}")
                
                # IMPORTANT: Wait for Claude to process and respond
                print(f"⏳ Waiting {self.response_wait_time}s for Claude to respond...")
                time.sleep(self.response_wait_time)
                
            except queue.Empty:
                continue
    
    def start(self):
        """Start processing"""
        self.running = True
        self.thread = threading.Thread(target=self.process_events, daemon=True)
        self.thread.start()
        print(f"🚀 Event handler started! (Response wait: {self.response_wait_time}s)")
    
    def stop(self):
        """Stop processing"""
        self.running = False
        print("🛑 Event handler stopped")
    
    def set_response_time(self, seconds):
        """Adjust wait time based on Claude's response speed"""
        self.response_wait_time = seconds
        print(f"⏱️ Response wait time set to {seconds}s")

# Demo
if __name__ == "__main__":
    handler = WorkingEventHandler()
    handler.start()
    
    print("\n🎮 Event Handler Demo")
    print("Events will be spaced out to allow Claude to respond")
    print("-" * 50)
    
    while True:
        print("\n1. Send test event")
        print("2. Send multiple events (queued)")
        print("3. Adjust response wait time")
        print("4. Show queue size")
        print("5. Exit")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            handler.add_event("test", "Single test event")
            
        elif choice == '2':
            print("Adding 3 events to queue...")
            handler.add_event("voice", "Hey Mimi, how are you?")
            handler.add_event("system", "Battery at 25%")
            handler.add_event("app", "User opened VS Code")
            print(f"Events will be sent with {handler.response_wait_time}s spacing")
            
        elif choice == '3':
            seconds = input("Enter wait time in seconds (current: {}): ".format(handler.response_wait_time))
            try:
                handler.set_response_time(float(seconds))
            except:
                print("Invalid number")
                
        elif choice == '4':
            print(f"📊 Queue size: {handler.event_queue.qsize()} events waiting")
            
        elif choice == '5':
            handler.stop()
            break

# avatar_display.py
"""
Simple avatar display window for Maid-MCP
Shows Mimi with selected pose and allows easy closing
"""

import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QCursor
import requests
from requests.exceptions import ConnectionError
import time

class AvatarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.state_url = "http://localhost:3338"
        self.current_pose = "idle"
        self.sprites = {}
        self.dragging = False
        self.drag_position = QPoint()
        self.mouse_press_pos = None  # Track where mouse was pressed
        self.has_moved = False  # Track if mouse moved during press
        
        self.init_ui()
        self.load_sprites()
        self.start_state_polling()
        
    def init_ui(self):
        """Initialize the UI"""
        # Window settings - transparent and always on top
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # No title bar
            Qt.WindowStaysOnTopHint | # Always on top
            Qt.Tool |                 # No taskbar icon
            Qt.WindowCloseButtonHint  # Allow closing
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Create sprite label
        self.sprite_label = QLabel(self)
        self.sprite_label.setScaledContents(True)
        layout.addWidget(self.sprite_label)
        
        # Set initial size and position
        self.resize(200, 300)
        self.move(1000, 100)  # Default position (top-right area)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
    def load_sprites(self):
        """Load all available sprites"""
        library_path = os.path.join(os.path.dirname(__file__), "library")
        if not os.path.exists(library_path):
            print(f"Library path not found: {library_path}")
            return
            
        for filename in os.listdir(library_path):
            if filename.endswith('.png'):
                sprite_name = filename.replace('.png', '')
                filepath = os.path.join(library_path, filename)
                pixmap = QPixmap(filepath)
                if not pixmap.isNull():
                    # Scale to window size while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        self.width(), self.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.sprites[sprite_name] = scaled_pixmap
                    print(f"Loaded sprite: {sprite_name}")
        
        # Set initial sprite
        self.set_sprite("idle")
        
    def set_sprite(self, pose_name):
        """Change the displayed sprite"""
        if pose_name in self.sprites:
            self.sprite_label.setPixmap(self.sprites[pose_name])
            self.current_pose = pose_name
            print(f"Set sprite to: {pose_name}")
        else:
            print(f"Sprite not found: {pose_name}")
            
    def start_state_polling(self):
        """Start polling for state changes"""
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_state)
        self.poll_timer.start(100)  # Check every 100ms
        
    def check_state(self):
        """Check for state updates from the server"""
        # Don't update state while dragging
        if self.dragging:
            return
            
        try:
            response = requests.get(f"{self.state_url}/state", timeout=0.5)
            if response.status_code == 200:
                state = response.json()
                
                # Check visibility and show/hide accordingly
                visible = state.get('visible', True)
                if visible and not self.isVisible():
                    self.show()
                elif not visible and self.isVisible():
                    self.hide()
                
                # Get animation from state
                animation = state.get('animation')
                
                # Handle animation if present
                if animation is not None and animation and animation.get('sequence'):
                    # Animation is active
                    sequence = animation['sequence']
                    fps = animation['fps']
                    loop = animation['loop']
                    
                    # Initialize start time if not set
                    if animation.get('start_time') is None:
                        animation['start_time'] = time.time()
                    
                    # Calculate current frame
                    elapsed = time.time() - animation['start_time']
                    total_frames = len(sequence)
                    frame_duration = 1.0 / fps
                    frame_number = int(elapsed / frame_duration)
                    
                    if loop:
                        # For looping animations, use modulo to wrap around
                        current_frame_index = frame_number % total_frames
                        pose = sequence[current_frame_index]
                        if pose != self.current_pose:
                            self.set_sprite(pose)
                    elif frame_number < total_frames:
                        # For non-looping, show frame if within range
                        pose = sequence[frame_number]
                        if pose != self.current_pose:
                            self.set_sprite(pose)
                    else:
                        # Non-looping animation finished, clear it and return to idle
                        requests.post(f"{self.state_url}/state", 
                                    json={'animation': None, 'pose': 'idle'},
                                    timeout=0.1)
                        self.set_sprite('idle')
                else:
                    # No animation or animation cleared, use regular pose
                    new_pose = state.get('pose', 'idle')
                    if new_pose != self.current_pose:
                        self.set_sprite(new_pose)
                
                # Update position
                if 'position' in state:
                    x = state['position'].get('x', self.x())
                    y = state['position'].get('y', self.y())
                    self.move(x, y)
                    
        except (ConnectionError, requests.RequestException):
            # Server not available, just continue
            pass
            
    # Mouse event handlers for dragging and closing
    def mousePressEvent(self, event):
        """Handle mouse press - start dragging or check for close"""
        if event.button() == Qt.LeftButton:
            self.mouse_press_pos = event.globalPos()
            self.has_moved = False
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                
        elif event.button() == Qt.RightButton:
            # Right-click to hide (not close)
            self.hide()
            # Update state on server
            try:
                requests.post(f"{self.state_url}/state", 
                            json={'visible': False},
                            timeout=0.1)
            except:
                pass
            
    def mouseMoveEvent(self, event):
        """Handle mouse move - drag window"""
        if event.buttons() == Qt.LeftButton and self.mouse_press_pos:
            # Check if mouse moved significantly (more than 5 pixels)
            if not self.has_moved:
                move_distance = (event.globalPos() - self.mouse_press_pos).manhattanLength()
                if move_distance > 5:
                    self.has_moved = True
                    self.dragging = True
                    # Change to pick_up sprite when starting to drag
                    if "pick_up" in self.sprites:
                        self.set_sprite("pick_up")
            
            if self.dragging:
                self.move(event.globalPos() - self.drag_position)
                
                # Update position on server
                try:
                    requests.post(f"{self.state_url}/state", 
                                json={'position': {'x': self.x(), 'y': self.y()}},
                                timeout=0.1)
                except:
                    pass
                
    def mouseReleaseEvent(self, event):
        """Handle mouse release - stop dragging or cancel animation"""
        if event.button() == Qt.LeftButton:
            if not self.has_moved and self.mouse_press_pos:
                # This was a click, not a drag - cancel animation and return to idle
                try:
                    requests.post(f"{self.state_url}/state", 
                                json={'pose': 'idle', 'animation': None},
                                timeout=0.1)
                    self.set_sprite('idle')
                    print("Left-click: Animation cancelled, returning to idle")
                except:
                    pass
            elif self.dragging:
                # This was a drag - stop dragging and check state
                self.dragging = False
                self.check_state()
            
            # Reset tracking variables
            self.mouse_press_pos = None
            self.has_moved = False
            
    def mouseDoubleClickEvent(self, event):
        """Double-click to close"""
        if event.button() == Qt.LeftButton:
            self.close()
            
    def keyPressEvent(self, event):
        """ESC key to close"""
        if event.key() == Qt.Key_Escape:
            self.close()
            
    def enterEvent(self, event):
        """Mouse enters window - show we're interactive"""
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
    def leaveEvent(self, event):
        """Mouse leaves window"""
        self.setCursor(QCursor(Qt.ArrowCursor))

def main():
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Maid Avatar")
    app.setQuitOnLastWindowClosed(True)
    
    # Create and show avatar
    avatar = AvatarWindow()
    avatar.show()
    
    # Add close instruction tooltip
    avatar.setToolTip("Left-click to cancel animation | Right-click to hide | Double-click to close\nDrag to move | ESC to close")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

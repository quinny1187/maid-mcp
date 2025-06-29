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
                
                # Update pose
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
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            
            # Change to pick_up sprite if available
            if "pick_up" in self.sprites:
                self.set_sprite("pick_up")
                
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
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            
            # Update position on server
            try:
                requests.post(f"{self.state_url}/state", 
                            json={'position': {'x': self.x(), 'y': self.y()}},
                            timeout=0.1)
            except:
                pass
                
    def mouseReleaseEvent(self, event):
        """Handle mouse release - stop dragging"""
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            # Return to previous sprite by checking server state
            self.check_state()
            
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
    avatar.setToolTip("Right-click to hide | Double-click to close permanently\nDrag to move | ESC to close")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

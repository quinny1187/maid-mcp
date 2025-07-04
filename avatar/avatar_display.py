# avatar_display_with_gif.py
"""
Avatar display window with GIF support for Maid-MCP
Shows Mimi with selected pose or animated GIFs
"""

import sys
import os
import json
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl, QByteArray, QBuffer, QSize
from PyQt5.QtGui import QPixmap, QCursor, QMovie
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
from requests.exceptions import ConnectionError
import time

class AvatarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.state_url = "http://localhost:3338"
        self.current_pose = "idle"
        self.current_animation_id = None
        self.current_gif_url = None
        self.sprites = {}
        self.dragging = False
        self.drag_position = QPoint()
        self.mouse_press_pos = None
        self.has_moved = False
        self.animation_start_times = {}  # Track animation start times locally
        self.last_pose_indices = {}  # Track last pose index for each animation
        
        # Network manager for downloading GIFs
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_gif_downloaded)
        
        # Movie for GIF playback
        self.movie = None
        self.gif_data = None
        self.gif_timer = None
        self.playing_gif = False
        
        # Store original window size
        self.normal_width = 200
        self.normal_height = 300
        
        self.init_ui()
        self.load_sprites()
        self.start_state_polling()
        
        # Set initial sprite after window is fully initialized
        QTimer.singleShot(50, lambda: self.set_sprite("idle"))
        
    def init_ui(self):
        """Initialize the UI"""
        # Window settings - transparent and always on top
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowCloseButtonHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Create sprite label
        self.sprite_label = QLabel(self)
        self.sprite_label.setAlignment(Qt.AlignCenter)
        self.sprite_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.sprite_label)
        
        # Set initial size and position
        self.resize(self.normal_width, self.normal_height)
        self.move(1000, 100)
        
        # Ensure transparent background
        self.setStyleSheet("background-color: transparent;")        
        
        # Enable mouse tracking
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
                    # Store original pixmap without scaling
                    self.sprites[sprite_name] = pixmap
                    print(f"Loaded sprite: {sprite_name}")
        
    def set_sprite(self, pose_name, animation_id=None):
        """Change the displayed sprite"""
        # Stop any playing GIF
        if self.movie:
            self.movie.stop()
            self.movie = None
            
        if pose_name in self.sprites:
            # Get the original pixmap
            pixmap = self.sprites[pose_name]
            
            # Scale to current window size
            target_width = self.width()
            target_height = self.height()
            
            # Only scale if window has valid size
            if target_width > 0 and target_height > 0:
                scaled_pixmap = pixmap.scaled(
                    target_width, target_height,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.sprite_label.setPixmap(scaled_pixmap)
            else:
                # Use original if window not ready
                self.sprite_label.setPixmap(pixmap)
                
            self.current_pose = pose_name
            
            if animation_id and animation_id != self.current_animation_id:
                self.current_animation_id = animation_id
        else:
            print(f"Sprite not found: {pose_name}")
            
    def download_gif(self, url):
        """Download a GIF from URL"""
        if url == self.current_gif_url:
            return  # Already downloading or downloaded
            
        self.current_gif_url = url
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)
        print(f"Downloading GIF: {url}")
        
    def on_gif_downloaded(self, reply):
        """Handle downloaded GIF data"""
        if reply.error() == QNetworkReply.NoError:
            self.gif_data = reply.readAll()
            self.show_gif()
        else:
            print(f"Error downloading GIF: {reply.errorString()}")
        reply.deleteLater()
        
    def show_gif(self):
        """Display the downloaded GIF"""
        if not self.gif_data:
            return
            
        # Temporarily double the width for GIF display
        self.resize(self.normal_width * 2, self.normal_height)
        
        # Save GIF to temporary file - sometimes QMovie works better with files
        try:
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
                tmp_file.write(self.gif_data)
                self.temp_gif_path = tmp_file.name
        except Exception as e:
            print(f"Error saving temp GIF: {e}")
            return
            
        # Create a movie from the file
        self.movie = QMovie(self.temp_gif_path)
        
        # For large GIFs, reduce quality to improve performance
        gif_size = os.path.getsize(self.temp_gif_path)
        if gif_size > 500000:  # If GIF is larger than 500KB
            print(f"Large GIF detected ({gif_size} bytes), optimizing for performance")
            # Don't cache all frames for large GIFs
            self.movie.setCacheMode(QMovie.CacheNone)
        else:
            # Force cache mode for smoother playback on small GIFs
            self.movie.setCacheMode(QMovie.CacheAll)
        
        # Set a reasonable cache limit
        self.movie.setScaledSize(QSize())  # Use original size, no scaling
        
        # Don't scale at all - let GIF play at original size
        # Center it in the label instead
        self.sprite_label.setScaledContents(False)
        self.sprite_label.setAlignment(Qt.AlignCenter)
        
        # Set the movie to the label
        self.sprite_label.setMovie(self.movie)
        
        # Connect frame updates to force widget updates
        # Commenting out aggressive frame updates - this might cause hiccups
        # self.movie.frameChanged.connect(self.on_gif_frame_changed)
        
        # Start playing at natural speed
        self.movie.setSpeed(100)  # Explicitly set to normal speed
        self.movie.start()
        
        # ENTER GIF MODE - Stop state polling for smooth playback
        self.poll_timer.stop()
        self.playing_gif = True
        
        # Clear any pending animations on the server and set pose to None
        try:
            requests.post(f"{self.state_url}/state", 
                        json={'animation': None, 'pose': None},
                        timeout=0.05)
        except:
            pass
        
        # Start a timer to check GIF duration
        # Duration comes from the server state
        self.gif_timer = QTimer()
        self.gif_timer.timeout.connect(self.check_gif_duration)
        self.gif_timer.start(1000)  # Check every second
        
        # Log the movie speed to debug
        print(f"GIF playing - Speed: {self.movie.speed()}% (100% is normal)")
        print(f"GIF frame count: {self.movie.frameCount()}")
        print(f"GIF loaded from temp file: {self.temp_gif_path}")
        print("Entered GIF MODE - State polling paused")
        
    def hide_gif(self):
        """Hide the GIF and restore avatar"""
        # Prevent multiple calls
        if not self.movie and not self.playing_gif:
            return  # Already hidden
            
        if self.movie:
            # Stop the movie
            self.movie.stop()
            self.movie = None
            self.current_gif_url = None
            self.gif_data = None
            
        # Clean up temporary file
        if hasattr(self, 'temp_gif_path') and os.path.exists(self.temp_gif_path):
            try:
                os.unlink(self.temp_gif_path)
            except:
                pass
            
        # Restore scaled contents setting for sprites
        self.sprite_label.setScaledContents(False)
        
        # Restore original window size
        self.resize(self.normal_width, self.normal_height)
        
        # Restore the avatar sprite with proper scaling
        self.set_sprite("idle")
        
        # Stop GIF duration timer if running
        if hasattr(self, 'gif_timer') and self.gif_timer:
            self.gif_timer.stop()
            self.gif_timer = None
            
        # EXIT GIF MODE - Restart state polling for animations
        self.playing_gif = False
        
        # Notify server to set pose back to idle
        try:
            requests.post(f"{self.state_url}/state", 
                        json={'pose': 'idle'},
                        timeout=0.1)
        except:
            pass
            
        # Wait a moment before restarting polling to ensure state is updated
        QTimer.singleShot(100, self.restart_polling)
        
        # Notify server
        try:
            requests.post(f"{self.state_url}/hide_gif", timeout=0.1)
        except:
            pass
            
    def start_state_polling(self):
        """Start polling for state changes"""
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_state)
        self.poll_timer.start(50)  # Check every 50ms for smoother animations
        
    def check_state(self):
        """Check for state updates from the server"""
        if self.dragging:
            return
            
        # Skip ALL state checking during GIF playback
        # This ensures smooth GIF performance
        if self.playing_gif:
            return
            
        try:
            response = requests.get(f"{self.state_url}/state", timeout=0.05)  # 50ms timeout for faster polling
            if response.status_code == 200:
                state = response.json()
                
                # Check visibility
                visible = state.get('visible', True)
                if visible and not self.isVisible():
                    self.show()
                elif not visible and self.isVisible():
                    self.hide()
                
                # Check for GIF
                gif_info = state.get('gif')
                if gif_info:
                    # GIF is active
                    gif_url = gif_info.get('url')
                    duration = gif_info.get('duration', 5)
                    self.gif_duration = duration
                    self.gif_start_time = gif_info.get('start_time', time.time())
                    
                    # Download and show GIF if not already showing
                    if gif_url and gif_url != self.current_gif_url:
                        self.download_gif(gif_url)
                    
                    # Check if GIF duration has expired
                    elapsed = time.time() - self.gif_start_time
                    if elapsed >= self.gif_duration:
                        self.hide_gif()
                        print(f"GIF duration expired ({self.gif_duration}s)")
                        return  # Exit early since we just hid the GIF
                else:
                    # No GIF, handle normal avatar display
                    if self.movie:
                        self.hide_gif()
                        return  # Exit early since we just hid the GIF
                    
                    # Handle animation
                    animation = state.get('animation')
                    if animation:
                        # Get sequence from either 'sequence' or 'frames' field
                        sequence = animation.get('sequence') or animation.get('frames', [])
                        if sequence:
                            # Animation logic
                            animation_id = animation.get('id', 'unknown')
                            fps = animation.get('fps', 2)
                            loop = animation.get('loop', False)
                        
                        # Use local start time tracking
                        if animation_id not in self.animation_start_times:
                            # First time seeing this animation, set start time
                            self.animation_start_times[animation_id] = time.time()
                            start_time = self.animation_start_times[animation_id]
                            print(f"\n[ANIMATION START] {animation_id}")
                            print(f"  Sequence: {sequence}")
                            print(f"  Total poses: {len(sequence)}")
                            # Use duration_per_pose if available, otherwise default to 2 seconds
                            duration_per_pose = animation.get('duration_per_pose', 2.0)
                            print(f"  Duration per pose: {duration_per_pose}s")
                            print(f"  Total duration: {len(sequence) * duration_per_pose:.1f}s")
                        else:
                            start_time = self.animation_start_times[animation_id]
                        
                        elapsed = time.time() - start_time
                        total_poses = len(sequence)
                        
                        # Get duration_per_pose or calculate from fps
                        if 'duration_per_pose' in animation:
                            duration_per_pose = animation['duration_per_pose']
                        elif fps > 0:
                            duration_per_pose = 1.0 / fps
                        else:
                            duration_per_pose = 2.0  # Default 2 seconds
                            
                        current_pose_index = int(elapsed / duration_per_pose)
                        time_in_current_pose = elapsed % duration_per_pose
                        
                        # Detailed pose logging (only log significant changes)
                        last_index = self.last_pose_indices.get(animation_id, -1)
                        if current_pose_index != last_index and current_pose_index < len(sequence):
                            pose_name = sequence[current_pose_index] if current_pose_index < len(sequence) else "unknown"
                            print(f"[POSE] {animation_id}: showing pose {current_pose_index} ({pose_name}) at {elapsed:.1f}s")
                            self.last_pose_indices[animation_id] = current_pose_index
                        
                        if loop:
                            # For looping animations, wrap around
                            current_pose_index = current_pose_index % total_poses
                            pose = sequence[current_pose_index]
                            if pose != self.current_pose:
                                print(f"  -> Setting pose: {pose} (pose {current_pose_index})")
                                self.set_sprite(pose, animation_id)
                        elif current_pose_index < total_poses:
                            # For non-looping, show current pose
                            pose = sequence[current_pose_index]
                            if pose != self.current_pose:
                                print(f"  -> Setting pose: {pose} (pose {current_pose_index})")
                                self.set_sprite(pose, animation_id)
                        else:
                            # Animation complete
                            print(f"\n[ANIMATION COMPLETE] {animation_id} after {elapsed:.3f}s")
                            # Clear local tracking
                            if animation_id in self.animation_start_times:
                                del self.animation_start_times[animation_id]
                            if animation_id in self.last_pose_indices:
                                del self.last_pose_indices[animation_id]
                            requests.post(f"{self.state_url}/state", 
                                        json={'animation': None, 'pose': 'idle'},
                                        timeout=0.1)
                            self.set_sprite('idle')
                    else:
                        # Regular pose
                        new_pose = state.get('pose', 'idle')
                        if new_pose and new_pose != self.current_pose and not self.movie:
                            self.set_sprite(new_pose)
                
                # Update position
                if 'position' in state:
                    x = state['position'].get('x', self.x())
                    y = state['position'].get('y', self.y())
                    self.move(x, y)
                    
        except (ConnectionError, requests.RequestException):
            pass
            
    # Mouse event handlers
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.LeftButton:
            self.mouse_press_pos = event.globalPos()
            self.has_moved = False
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                
        elif event.button() == Qt.RightButton:
            # Right-click to hide
            self.hide()
            try:
                requests.post(f"{self.state_url}/state", 
                            json={'visible': False},
                            timeout=0.1)
            except:
                pass
            
    def mouseMoveEvent(self, event):
        """Handle mouse move - drag window"""
        if event.buttons() == Qt.LeftButton and self.mouse_press_pos:
            if not self.has_moved:
                move_distance = (event.globalPos() - self.mouse_press_pos).manhattanLength()
                if move_distance > 5:
                    self.has_moved = True
                    self.dragging = True
                    if "pick_up" in self.sprites and not self.movie:
                        self.set_sprite("pick_up")
            
            if self.dragging:
                self.move(event.globalPos() - self.drag_position)
                
                try:
                    requests.post(f"{self.state_url}/state", 
                                json={'position': {'x': self.x(), 'y': self.y()}},
                                timeout=0.1)
                except:
                    pass
                
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            if not self.has_moved and self.mouse_press_pos:
                # Click - cancel animation or hide GIF
                if self.movie:
                    self.hide_gif()
                    print("Left-click: GIF hidden")
                else:
                    try:
                        # Clear any animation tracking when cancelling
                        self.animation_start_times.clear()
                        self.last_pose_indices.clear()
                        requests.post(f"{self.state_url}/state", 
                                    json={'pose': 'idle', 'animation': None},
                                    timeout=0.1)
                        self.set_sprite('idle')
                        self.current_animation_id = None
                        print("Left-click: Animation cancelled")
                    except:
                        pass
            elif self.dragging:
                self.dragging = False
                self.check_state()
            
            self.mouse_press_pos = None
            self.has_moved = False
            
    def mouseDoubleClickEvent(self, event):
        """Double-click to close"""
        if event.button() == Qt.LeftButton:
            self.close()
            
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Refresh current sprite when window is resized
        if self.current_pose and not self.movie:
            self.set_sprite(self.current_pose)
            
    def keyPressEvent(self, event):
        """ESC key to close"""
        if event.key() == Qt.Key_Escape:
            self.close()
            
    def on_gif_frame_changed(self, frame_number):
        """Force update when GIF frame changes"""
        # Force the widget to repaint
        self.sprite_label.update()
        self.update()
        
    def restart_polling(self):
        """Restart state polling after GIF mode"""
        # Clear any animation tracking since we were in GIF mode
        self.animation_start_times.clear()
        self.last_pose_indices.clear()
        
        self.poll_timer.start(50)  # Resume at 50ms for smooth animations
        print("Exited GIF MODE - State polling resumed")
        
        # Log current state
        try:
            response = requests.get(f"{self.state_url}/state", timeout=0.05)
            if response.status_code == 200:
                state = response.json()
                animation = state.get('animation')
                print(f"State after GIF: animation={animation}, pose={state.get('pose', 'unknown')}")
        except:
            pass
        
    def check_gif_duration(self):
        """Check if GIF duration has expired"""
        # Only check if we're actually playing a GIF
        if not self.playing_gif or not self.movie:
            # Stop the timer if GIF already ended
            if self.gif_timer:
                self.gif_timer.stop()
            return
            
        # Get the latest state to check duration
        try:
            response = requests.get(f"{self.state_url}/state", timeout=0.05)
            if response.status_code == 200:
                state = response.json()
                gif_info = state.get('gif')
                if gif_info:
                    duration = gif_info.get('duration', 5)
                    start_time = gif_info.get('start_time', time.time())
                    elapsed = time.time() - start_time
                    if elapsed >= duration:
                        self.hide_gif()
                        print(f"GIF duration expired ({duration}s)")
                else:
                    # GIF was removed from state
                    self.hide_gif()
                    print("GIF removed from state")
        except:
            pass
            
    def enterEvent(self, event):
        """Mouse enters window"""
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
    def leaveEvent(self, event):
        """Mouse leaves window"""
        self.setCursor(QCursor(Qt.ArrowCursor))

def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("Maid Avatar with GIF")
    app.setQuitOnLastWindowClosed(True)
    
    avatar = AvatarWindow()
    avatar.show()
    
    avatar.setToolTip("Left-click to cancel animation/hide GIF | Right-click to hide | Double-click to close\nDrag to move | ESC to close\nGIFs display in expanded window")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

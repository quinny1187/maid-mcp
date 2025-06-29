# avatar_state_server.py
"""
Simple state server for avatar coordination
Runs on http://localhost:3338
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import time

app = Flask(__name__)
CORS(app)

# Disable Flask logging for cleaner output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Global state
avatar_state = {
    'visible': True,
    'pose': 'idle',
    'position': {'x': 1000, 'y': 100},
    'last_update': None,
    'animation': None  # Animation data
}

@app.route('/state', methods=['GET'])
def get_state():
    """Get current avatar state"""
    return jsonify(avatar_state)

@app.route('/state', methods=['POST'])
def update_state():
    """Update avatar state"""
    global avatar_state
    
    data = request.get_json()
    print(f"[DEBUG] Received state update: {data}")  # Debug log
    
    if data:
        # Handle animation clearing explicitly
        if 'animation' in data and data['animation'] is None:
            avatar_state['animation'] = None
            print("Animation cleared")
        
        avatar_state.update(data)
        
        # Log state changes
        if 'pose' in data:
            print(f"Avatar pose changed to: {data['pose']}")
        if 'visible' in data:
            print(f"Avatar visibility: {data['visible']}")
        if 'position' in data:
            print(f"Avatar moved to: {data['position']}")
        if 'animation' in data and data['animation'] is not None:
            print(f"Animation updated: {data['animation']}")
    
    return jsonify({'status': 'ok'})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'running'})

@app.route('/play_animation', methods=['POST'])
def play_animation():
    """Play an animation with clean logging"""
    global avatar_state
    
    data = request.get_json()
    if data:
        # Store animation data with current time
        avatar_state['animation'] = {
            'id': data.get('id'),
            'name': data.get('name'),
            'sequence': data.get('frames', []),
            'fps': data.get('fps', 2),
            'loop': data.get('loop', False),
            'current_frame': 0,
            'start_time': time.time()
        }
        
        # Make avatar visible when animation starts
        avatar_state['visible'] = True
        
        # Clean log - just the animation name
        print(f"Playing animation: {data.get('name', data.get('id'))}")
    
    return jsonify({'status': 'ok'})

@app.route('/animate', methods=['DELETE'])
def stop_animation():
    """Stop current animation"""
    global avatar_state
    
    avatar_state['animation'] = None
    avatar_state['pose'] = 'idle'  # Return to idle
    
    print("Animation stopped")
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Avatar State Server running on http://localhost:3338")
    print("Endpoints:")
    print("  GET  /state - Get current state")
    print("  POST /state - Update state")
    print("  GET  /health - Health check")
    print("  POST /play_animation - Play animation")
    print("  DELETE /animate - Stop animation")
    app.run(host='0.0.0.0', port=3338, debug=False)

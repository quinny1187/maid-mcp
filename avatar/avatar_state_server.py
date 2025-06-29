# avatar_state_server.py
"""
Simple state server for avatar coordination
Runs on http://localhost:3338
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

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
    'last_update': None
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
    if data:
        avatar_state.update(data)
        
        # Log state changes
        if 'pose' in data:
            print(f"Avatar pose changed to: {data['pose']}")
        if 'visible' in data:
            print(f"Avatar visibility: {data['visible']}")
        if 'position' in data:
            print(f"Avatar moved to: {data['position']}")
    
    return jsonify({'status': 'ok'})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    print("Avatar State Server running on http://localhost:3338")
    print("Endpoints:")
    print("  GET  /state - Get current state")
    print("  POST /state - Update state")
    print("  GET  /health - Health check")
    app.run(host='0.0.0.0', port=3338, debug=False)

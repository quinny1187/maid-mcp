# Auto Claude - Programmatic Claude Desktop Control

These Python scripts allow sending messages to Claude Desktop programmatically.

## Files

### ultra_fast_sender.py
- Ultra-fast message sender using UI Automation
- Sends messages with minimal delay (<200ms)
- Uses pywinauto to control Claude Desktop

### working_event_handler.py
- Event queue system for managing multiple messages
- Waits for Claude to respond before sending next message
- Default 5 second wait between messages
- Supports different event types (voice, system, app)

## Requirements
```
pip install pywinauto
pip install pywin32
```

## Usage

### Quick send:
```python
from ultra_fast_sender import send_to_claude
send_to_claude("Hello Claude!")
```

### Event queue:
```python
python working_event_handler.py
```

## Note
These scripts were created before MCP (Model Context Protocol) was available. 
Now that MCP exists, the voice functionality has been implemented as an MCP tool instead.
These scripts remain useful for programmatically controlling Claude Desktop when needed.

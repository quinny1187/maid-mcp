# Start-All Process Management Fix

## Issue
Multiple avatar screens were being created when running start-all.bat because existing processes weren't being properly terminated before starting new ones.

## Solution Implemented

### 1. Enhanced start_all.bat
- Now calls stop_all.bat first to ensure clean shutdown
- Added multiple cleanup methods:
  - Window title matching
  - WMIC process killing by command line
  - Port 3338 cleanup
  - PowerShell backup cleanup
- Increased wait time to 3 seconds for process termination
- Better error handling and user feedback

### 2. Created start_all_python.bat
- Uses the Python launcher (start_all.py) with psutil
- Automatically checks for and installs psutil if missing
- Provides the most reliable process management
- Recommended approach for best results

### 3. Improved stop_all.bat
- 5-step comprehensive cleanup process
- Shows progress for each step
- Verifies port 3338 is freed after cleanup
- Forceful retry if processes remain

## Usage

### Option 1: Use Python Launcher (Recommended)
```batch
start_all_python.bat
```
This uses psutil for proper process detection and termination.

### Option 2: Use Enhanced Batch File
```batch
start_all.bat
```
This has improved cleanup but may miss some edge cases.

### To Stop All Systems
```batch
stop_all.bat
```

## Technical Details

The Python launcher (start_all.py) uses psutil to:
- Find processes by command line arguments
- Kill processes using specific ports
- Ensure clean termination before starting new instances

The batch files use:
- taskkill with window title filters
- WMIC for command-line based process killing  
- netstat to find processes using port 3338
- PowerShell as a backup method

This multi-layered approach ensures no duplicate avatar screens will appear when restarting the system.

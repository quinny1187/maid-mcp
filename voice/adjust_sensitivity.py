"""
Update voice sensitivity configuration
"""

import configparser
import os

def update_sensitivity():
    config_path = os.path.join('voice', 'incoming', 'voice_config.ini')
    
    # Read current config
    config = configparser.ConfigParser()
    config.read(config_path)
    
    current = config.get('recognition', 'energy_threshold', fallback='4000')
    
    print("=" * 50)
    print("  Voice Sensitivity Adjustment")
    print("=" * 50)
    print(f"\nCurrent energy_threshold: {current}")
    print()
    print("Choose a new sensitivity level:")
    print()
    print("1. Very Sensitive (2000) - Picks up whispers")
    print("2. Sensitive (4000) - Normal quiet room")
    print("3. Moderate (6000) - Average room")
    print("4. Less Sensitive (8000) - Recommended for most")
    print("5. Very Insensitive (10000) - Noisy environment")
    print("6. Custom value")
    print()
    
    choice = input("Enter your choice (1-6): ")
    
    thresholds = {
        '1': '2000',
        '2': '4000',
        '3': '6000',
        '4': '8000',
        '5': '10000'
    }
    
    if choice in thresholds:
        new_threshold = thresholds[choice]
    elif choice == '6':
        new_threshold = input("Enter custom threshold value: ")
        try:
            int(new_threshold)  # Validate it's a number
        except:
            print("Invalid value! Using default 4000")
            new_threshold = '4000'
    else:
        print("Invalid choice! No changes made.")
        return
    
    # Update config
    if 'recognition' not in config:
        config['recognition'] = {}
    
    config['recognition']['energy_threshold'] = new_threshold
    
    # Write back
    with open(config_path, 'w') as f:
        config.write(f)
    
    print()
    print(f"✓ Sensitivity updated to {new_threshold}")
    print()
    print("Please restart the voice input system for changes to take effect.")

if __name__ == "__main__":
    update_sensitivity()
    input("\nPress Enter to exit...")

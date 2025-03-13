import re
import json
import csv
import pyautogui
import pytesseract
from PIL import Image, ImageGrab, ImageEnhance
import time
import win32gui
import win32con
import os

def find_tesseract_executable():
    # Common base directories to start the search
    user_home = os.path.expanduser('~')
    base_dirs = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        user_home,  # User's home directory
        os.path.join(user_home, 'Desktop'),
        os.path.join(user_home, 'Downloads'),
        os.path.join(user_home, 'OneDrive'),
        os.path.join(user_home, 'OneDrive', 'Desktop'),
        "C:\\",  # Root directory as last resort
    ]
    
    # First, check the known path directly
    known_path = os.path.join(user_home, 'OneDrive', 'Desktop', 'tesseract-OCR', 'tesseract.exe')
    if os.path.exists(known_path):
        print(f"Found Tesseract at known path: {known_path}")
        return known_path
    
    # Cache file to store the found path
    cache_file = 'tesseract_path_cache.txt'
    
    # Check if we have a cached path
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_path = f.read().strip()
            if os.path.exists(cached_path):
                print(f"Using cached Tesseract path: {cached_path}")
                return cached_path
    
    print("Searching for Tesseract executable... This might take a moment.")
    
    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
            
        for root, dirs, files in os.walk(base_dir):
            # Skip some common directories that won't contain Tesseract
            if any(skip in root.lower() for skip in [
                'windows', 'system32', 'programdata', 'appdata',
                '$recycle.bin', 'program files\\common files'
            ]):
                continue
                
            if 'tesseract.exe' in files and 'Tesseract-OCR' in root:
                tesseract_path = os.path.join(root, 'tesseract.exe')
                print(f"Found Tesseract at: {tesseract_path}")
                
                # Cache the found path
                with open(cache_file, 'w') as f:
                    f.write(tesseract_path)
                    
                return tesseract_path
    
    return None

# Find Tesseract executable
tesseract_path = find_tesseract_executable()

if tesseract_path is None:
    raise Exception(
        "Tesseract not found. Please install it from: https://github.com/UB-Mannheim/tesseract/wiki\n"
        "Or manually add its path to the tesseract_path variable."
    )

pytesseract.pytesseract.tesseract_cmd = tesseract_path

def find_showdown_window():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Showdown!" in title:
                windows.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None


def capture_chat():
    # Find and focus Pokemon Showdown window
    showdown_window = find_showdown_window()
    if not showdown_window:
        raise Exception("Pokemon Showdown window not found!")
    
    # Maximize the window and wait for it to complete
    win32gui.ShowWindow(showdown_window, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(showdown_window)
    time.sleep(1.5)  # Increased wait time for window to properly maximize
    
    # Get window coordinates after maximizing
    window_rect = win32gui.GetWindowRect(showdown_window)
    window_x = window_rect[0]
    window_y = window_rect[1]
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    
    # Ensure window is properly sized
    if window_width < 800 or window_height < 600:  # minimum size check
        raise Exception("Window is too small, please ensure Pokemon Showdown is properly maximized")
    
    # Calculate chat area with adjusted position and height
    chat_width = window_width // 3 + 100  # Keep same width
    chat_x = (window_x + window_width // 2) - 170  # Keep same x position
    chat_y = window_y + 100  # Start higher up
    chat_height = 900  # Fixed height to capture about 12-13 lines of chat
    
    # Capture the specified region
    chat_area = ImageGrab.grab(bbox=(chat_x, chat_y, chat_width + chat_x, chat_height + chat_y))
    
    # Image preprocessing for better OCR
    if chat_area.mode != 'RGB':
        chat_area = chat_area.convert('RGB')
    
    # Increase image size by 2x for better recognition
    width, height = chat_area.size
    chat_area = chat_area.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(chat_area)
    chat_area = enhancer.enhance(1.5)  # Increase contrast by 50%
    
    # Save screenshot for debugging (optional)
    chat_area.save('debug/debug_screenshot.png')
    
    # Configure Tesseract parameters for better accuracy
    custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1 -c tessedit_char_blacklist=|'
    
    # Convert image to text using OCR with custom config
    text = pytesseract.image_to_string(chat_area, config=custom_config)
    
    # Post-process common OCR mistakes
    text = text.replace('fel', 'fell')  # Fix common 'fell' misread
    text = text.replace('felll', 'fell')  # Fix triple 'l' issue
    text = text.replace('Iey', 'Icy')   # Fix common 'Icy' misread
    text = re.sub(r'(\d+),(\d+)', r'\1.\2', text)  # Fix comma/decimal point confusion
    
    # Remove single character lines and special characters
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if (len(line) <= 1 or 
            line.isspace() or 
            all(not c.isalnum() for c in line)):
            continue
        line = re.sub(r'[^\w\s%\.!\[\]()-]', '', line)
        lines.append(line)
    
    # Initialize turn counter
    turn_counter = 0
    battle_started = False

    # Find the battle start line and turn line(s)
    battle_start_idx = None
    turn_indices = []
    for i, line in enumerate(lines):
        if "Battle started between" in line:
            battle_start_idx = i
            battle_started = True
        if battle_started and re.match(r'Turn \d+', line):  # Match lines like "Turn 1", "Turn 2", etc.
            turn_indices.append(i)
    
    # If we found a battle start line, extract between it and the next turn line
    if battle_start_idx is not None:
        if turn_indices:
            start_idx = battle_start_idx
            end_idx = turn_indices[0]  # Get the index of the first "Turn X"
            content_lines = lines[start_idx + 1:end_idx]  # Extract lines between
            turn_counter += 1  # Increment turn counter after capturing
            
            # Check for the next turn if needed
            if len(turn_indices) > 1:
                next_turn_start_idx = turn_indices[1]
                next_turn_content = lines[end_idx + 1:next_turn_start_idx]  # Capture text until the next turn
                content_lines.extend(next_turn_content)  # Append the next turn content
        else:
            # If no turn indices found, capture everything after battle start
            content_lines = lines[battle_start_idx + 1:]
    else:
        content_lines = []

    # Filter unwanted words and expired messages
    unwanted_words = ['left', 'joined']
    
    cleaned_lines = [
        line 
        for line in content_lines 
        if not any(word in line.lower() for word in unwanted_words)
    ]
    
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Debug information
    print("Debug - Original text:")
    print(text)
    print("\nDebug - Markers found:")
    print(f"Battle start index: {battle_start_idx}")
    print(f"Turn markers found at: {turn_indices}")
    
    return cleaned_text

def main():
    try:
        print("Looking for Pokemon Showdown window...")
        chat_text = capture_chat()
        
        # Print the extracted text
        print("Extracted chat text:")
        print("-" * 50)
        print(chat_text)
        
        # Save to file
        with open('debug/chat_log.txt', 'w', encoding='utf-8') as f:
            f.write(chat_text)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

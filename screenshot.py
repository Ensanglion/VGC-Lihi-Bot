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
    # Convert to RGB if needed
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
        # Skip empty lines, single characters, or lines with just special characters
        if (len(line) <= 1 or 
            line.isspace() or 
            all(not c.isalnum() for c in line)):
            continue
        # Clean up any remaining special characters
        line = re.sub(r'[^\w\s%\.!\[\]()-]', '', line)
        lines.append(line)
    
    # Define patterns
    turn_pattern = re.compile(r'.*(?:turn|tum|torn|tumn)\s*\d+.*', re.IGNORECASE)
    users_pattern = re.compile(r'.*\d+\s*users?.*', re.IGNORECASE)  # Match both "user" and "users"
    
    # Function to check if a string might be a garbled "this room is expired" message
    def is_expired_message(text):
        # Convert to lowercase and remove special characters for comparison
        cleaned = re.sub(r'[^\w\s]', '', text.lower())
        words = cleaned.split()
        
        # Common OCR misreadings we've seen
        if any(w in ['thic', 'this', 'thi', 'th'] for w in words) and \
           any(w in ['ranm', 'room', 'rom', 'rm'] for w in words) and \
           any(w in ['ic', 'is', 'i'] for w in words) and \
           any(w in ['avnirod', 'expired', 'expird', 'expir'] for w in words):
            return True
        return False
    
    # Find markers
    start_idx = None
    end_idx = None
    
    # First try to find two turn markers
    turn_indices = []
    expired_idx = None
    
    for i, line in enumerate(lines):
        if turn_pattern.search(line):
            turn_indices.append(i)
            if len(turn_indices) == 2:  # Found two turn markers
                start_idx = turn_indices[0]
                end_idx = turn_indices[1]
                break
        elif is_expired_message(line):  # Use the new function instead of expired_pattern
            expired_idx = i
    
    # If we didn't find two turn markers but found one
    if len(turn_indices) == 1:
        turn_idx = turn_indices[0]
        # Check if there's a users line immediately before the turn
        if turn_idx > 0 and users_pattern.search(lines[turn_idx - 1]):
            # Users line is right before turn, so start from turn
            start_idx = turn_idx
        else:
            # No users line or not immediately before, use turn as normal
            start_idx = turn_idx
        
        # If we found an "expired" message, use it as the end marker
        if expired_idx is not None and expired_idx > turn_idx:
            end_idx = expired_idx
        else:
            end_idx = None
    
    # If we didn't find any turn markers but found a users line, try to use that
    if not turn_indices and not start_idx:
        for i, line in enumerate(lines):
            if users_pattern.search(line):
                start_idx = i
                if expired_idx is not None and expired_idx > i:
                    end_idx = expired_idx
                break
    
    # Filter out unwanted words from the relevant section
    unwanted_words = ['left', 'joined']  # Removed 'expired' since we're using the function now
    
    if start_idx is not None:
        if end_idx is not None:
            # Take text between markers
            content_lines = lines[start_idx + 1:end_idx]
        else:
            # Take text after start marker to the end
            content_lines = lines[start_idx + 1:]
            
        # Filter unwanted words and expired messages
        cleaned_lines = [
            line 
            for line in content_lines 
            if not any(word in line.lower() for word in unwanted_words)
            and not is_expired_message(line)  # Use the new function
        ]
        
        cleaned_text = '\n'.join(cleaned_lines)
    else:
        cleaned_text = ""
    
    # Debug information
    print("Debug - Original text:")
    print(text)
    print("\nDebug - Markers found:")
    print(f"Start index: {start_idx}")
    print(f"End index: {end_idx}")
    print(f"Turn markers found at: {turn_indices}")
    print(f"Expired marker found at: {expired_idx}")
    
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

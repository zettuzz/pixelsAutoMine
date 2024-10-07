import cv2
import numpy as np
import pyautogui
from PIL import Image
import time
import keyboard  # to capture keypress events

# Load the template images and convert to grayscale
template_img1 = cv2.imread('needle.png', cv2.IMREAD_GRAYSCALE)
template_img2 = cv2.imread('needle2.png', cv2.IMREAD_GRAYSCALE)

# Check if the templates were loaded successfully
if template_img1 is None or template_img2 is None:
    raise FileNotFoundError("One or both template images could not be found or opened.")

# Get dimensions for both templates
w1, h1 = template_img1.shape[1], template_img1.shape[0]
w2, h2 = template_img2.shape[1], template_img2.shape[0]

# Function to capture the entire screen
def capture_screen():
    # Take a screenshot using PyAutoGUI
    screenshot = pyautogui.screenshot() 

    # Convert the screenshot to a NumPy array for OpenCV processing
    screenshot_np = np.array(screenshot)

    # Convert RGB (PyAutoGUI uses RGB) to grayscale
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    return screenshot_np

# Function to find the template (needle) in the captured screen
def find_target(screenshot, template_img, threshold=0.8):
    # Perform template matching using OpenCV
    result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED)

    # Find where the matches exceed the threshold
    yloc, xloc = np.where(result >= threshold)

    # Return all matched positions
    if len(xloc) > 0:
        return list(zip(xloc, yloc))  # Return as a list of (x, y) coordinates
    else:
        return []

# Function to perform a mouse click at the target location
def perform_click(x, y, w, h, double_click=False):
    # Move the mouse to the center of the detected match and click
    pyautogui.moveTo(x + w // 2, y + h // 2)  # Move to the center of the found target
    pyautogui.click()
    if double_click:
        pyautogui.click()

# Function to perform scanning and clicking for a given template
def scan_and_click_consecutive(template_img1, w1, h1, template_img2, w2, h2):
    while True:
        # Step 1: Capture the screen
        screen_img = capture_screen()

        # Step 2: Search for the first template
        locations1 = find_target(screen_img, template_img1)
        if locations1:
            for loc in locations1:
                print(f"First target found at {loc}. Performing click.")
                perform_click(loc[0], loc[1], w1, h1)
        
        # Step 3: Search for the second template
        locations2 = find_target(screen_img, template_img2)
        if locations2:
            for loc in locations2:
                print(f"Second target found at {loc}. Performing click.")
                perform_click(loc[0], loc[1], w2, h2)
        
        # Step 4: Check if the user has pressed 'P' to stop the loop
        if keyboard.is_pressed('p'):
            print("Stopping process...")
            break

        # Wait for a short while before the next loop to avoid high CPU usage
        time.sleep(1)

# Main loop to capture the screen, search for template, and click
def main():
    print("Press 'P' to stop the process.")
    
    # Call the scan_and_click_consecutive function for each template
    scan_and_click_consecutive(template_img1, w1, h1, template_img2, w2, h2)

if __name__ == '__main__':
    main()

import time
import cv2
import numpy as np
import pytesseract
import pyautogui
import pygetwindow as gw

# Configure the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path as needed

def capture_specific_window(title):
    # Attempt to find the window with the specified title
    windows = gw.getWindowsWithTitle(title)
    if windows:
        window = windows[0]  # Take the first window that matches the title
        if window.isMinimized:
            window.restore()
        window.activate()  # Bring the window to the foreground

        # Wait briefly for the window to become active
        time.sleep(0.2)

        # Capture the window using its bounds
        x, y, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        return screenshot
    else:
        print("No window found with title:", title)
        return None

def apply_template_matching(template_image, method=cv2.TM_CCOEFF_NORMED):
    main_image = capture_specific_window("SDK V1.0.0.24")
    if main_image is None:
        print("No active window detected.")
        return None

    # Read the template
    template = cv2.imread(template_image, 0)  # Read in grayscale

    # Store the width and height of the template
    w, h = template.shape[::-1]

    # Convert main_image to grayscale
    main_image_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

    # Apply template Matching
    # Apply template Matching
    res = cv2.matchTemplate(main_image_gray, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    # Manually adjust the rectangle around the number
    # Calculate offsets to center the number (adjust these values as needed)
    offsetX = int(w * -0.01)  # Offset 10% of the width to the right
    offsetY = int(h * 0.15)  # Offset 30% of the height downward
    widthNum = int(w * 0.65)  # Number's width is 80% of the full width
    heightNum = int(h * 0.45)  # Number's height is 40% of the full height

    new_top_left = (top_left[0] + offsetX, top_left[1] + offsetY)
    new_bottom_right = (new_top_left[0] + widthNum, new_top_left[1] + heightNum)

    # Draw a rectangle on the image
    cv2.rectangle(main_image_gray, new_top_left, new_bottom_right, 150, 2)

    # Extract the matched region and save it
    matched_region = main_image_gray[max(0, new_top_left[1]):new_bottom_right[1], max(0, new_top_left[0]):new_bottom_right[0]]
    cv2.imwrite('matched_region.png', matched_region)

    return 'matched_region.png'

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert the image colors if needed (comment out if inversion is not useful)
    inverted = cv2.bitwise_not(gray)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    return thresh

def extract_numbers(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Use Tesseract to extract numbers
    custom_config = r'--oem 3 --psm 3 outputbase digits'  
    numbers = pytesseract.image_to_string(processed_image, config=custom_config)
    
    return numbers

def continuous_capture():
    template_image_path = 'D:/Stage Air 2024/AutoExtract+Behavior/test2.png'
    try:
        while True:
            matched_image_path = apply_template_matching(template_image_path)
            if matched_image_path:
                numbers = extract_numbers(matched_image_path)
                print("Detected numbers:", numbers)
            else:
                print("Failed to match template.")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Program stopped by user.")

continuous_capture()

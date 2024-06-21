import pyautogui
import time
     

def find_button(image_path, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if location:
            return location
        time.sleep(0.5)  
    raise Exception(f"Button not found: {image_path}")

def click_button(image_path):
    button_location = find_button(image_path)
    if button_location:
        pyautogui.click(button_location)
    else:
        raise Exception("Failed to click the button. Button not found.")
    
def test_button_detection():
    try:
        location = pyautogui.locateCenterOnScreen('write_settings.png', confidence=0.8)
        assert location is not None, "Button detection failed."
        print("Test Passed: Button detected.")
    except Exception as e:
        print("Test Failed:", str(e))


def test_button_click():
    try:
        location = pyautogui.locateCenterOnScreen('write_settings.png', confidence=0.8)
        assert location is not None, "Button not found for clicking."
        pyautogui.click(location)
        print("Test Passed: Button clicked successfully.")
    except Exception as e:
        print("Test Failed:", str(e))



def test_non_existent_button():
    try:
        location = find_button('non_existent_button.png')
        assert location is None, "Non-existent button should not be found."
    except Exception as e:
        print("Test Passed: Proper error handling for non-existent button.")



def automate_logging_process():
    try:
        wait_hours = float(input("Enter the duration for logging in hours: "))
        time.sleep(5)
        click_button('maximize_button.png')
        time.sleep(2)
        click_button('write_settings.png')
        time.sleep(2)  

        click_button('start_logging.png')
        print("Logging started. Waiting for specified duration...")

        time.sleep(wait_hours * 3600)  
        click_button('stop_logging.png')
        print("Logging stopped.")

        click_button('save_data.png')
        print("Data saved successfully.")
    except Exception as e:
        print(str(e))

automate_logging_process()







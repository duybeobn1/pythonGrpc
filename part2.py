import cv2
import pytesseract

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust as necessary

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast using histogram equalization
    equalized = cv2.equalizeHist(gray)

    # Apply Gaussian Blurring to reduce noise
    blur = cv2.GaussianBlur(equalized, (5, 5), 0)

    # Binarize the image using Otsu's thresholding
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def extract_numbers(image_path):
    # Preprocess the image to prepare for OCR
    processed_image = preprocess_image(image_path)

    # Use Tesseract to extract numbers
    custom_config = r'--oem 3 --psm 7 outputbase digits'  # Change psm to 7 assuming a single text line
    extracted_text = pytesseract.image_to_string(processed_image, config=custom_config)

    return extracted_text

# Path to the image that you uploaded
image_path = 'matched_region.png'  # Adjust the path as necessary

# Extract numbers
numbers = extract_numbers(image_path)
print(numbers)

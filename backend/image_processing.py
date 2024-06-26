import cv2
import pytesseract
import numpy as np

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image was successfully loaded
    if image is None:
        raise ValueError("Failed to load image from {}".format(image_path))

    # Convert the image to BGR color space (if it's not already in BGR)
    if len(image.shape) < 3 or image.shape[2] < 3:
        raise ValueError("Input image must be in BGR format with at least 3 channels")
    elif image.shape[2] > 3:
        # If the image has more than 3 channels, discard the extra channels
        image = image[:, :, :3]

     # Apply Gaussian blur to reduce noise (keep the image in BGR format)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    return blurred

def extract_text(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use Tesseract OCR to extract text from the preprocessed image
    text = pytesseract.image_to_string(image)
    return text

def detect_highlights(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for yellow color (highlighter)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Create a mask to isolate yellow regions (highlighted text)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply morphological operations to remove noise and fill gaps in the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask

def extract_highlighted_text(image_path):
    # Preprocess the image
    image = preprocess_image(image_path)

    # Detect highlighted regions in the image
    mask = detect_highlights(image)

    # Extract text from each highlighted region
    highlighted_text = ""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the highlighted region
        roi = image[y:y+h, x:x+w]

        # Extract text from the cropped region
        text = pytesseract.image_to_string(roi)

        # Append extracted text to the result
        highlighted_text += text + "\n"

    return highlighted_text

import cv2
import pytesseract
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

def detect_highlights(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return mask

def extract_highlighted_text(image_path):
    image = cv2.imread(image_path)
    mask = detect_highlights(image)
    highlighted_text = ""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y+h, x:x+w]
        highlighted_text += pytesseract.image_to_string(roi)
    return highlighted_text

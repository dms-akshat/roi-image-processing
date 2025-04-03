import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from django.conf import settings

def process_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the image. Check the file format and path.")

    height, width, _ = img.shape
    median_filtered_image = cv2.medianBlur(img, 5)
    hsv = cv2.cvtColor(median_filtered_image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 100, 50])
    upper_bound = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((5, 5), np.uint8)
    opened_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    edges = cv2.Canny(opened_mask, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 0.000008 * height * width
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    if filtered_contours:
        combined_contours = np.concatenate(filtered_contours)
        x, y, w, h = cv2.boundingRect(combined_contours)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi = img[y:y+h, x:x+w]
    else:
        # Return original image instead of None to avoid errors
        return image_path, 0  

    resized = cv2.resize(roi, (width, height), interpolation=cv2.INTER_LINEAR)
    score = ssim(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY))

    output_dir = os.path.join(settings.MEDIA_ROOT, "processed")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, resized)

    return output_path, score

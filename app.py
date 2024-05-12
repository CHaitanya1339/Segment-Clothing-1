from SegCloth import segment_clothing
from PIL import Image
import cv2
import numpy as np

# Load a sample image file instead of opening camera
sample_image_path = 'black.jpeg'
image = Image.open(sample_image_path)

result = segment_clothing(img=image, clothes= ["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"])

def check_color_presence(image, target_color_bgr, threshold_percentage):
    # Convert PIL Image to numpy array
    image_np = np.array(image.convert('RGB'))  # Ensure image is in RGB format
    if image_np is None:
        raise ValueError("Image not found or path is incorrect")

    tolerance = 150  # Adjust this based on how strict the color match should be

    lower_bound = np.array([max(0, target_color_bgr[0] - tolerance), max(0, target_color_bgr[1] - tolerance), max(0, target_color_bgr[2] - tolerance)])
    upper_bound = np.array([min(255, target_color_bgr[0] + tolerance), min(255, target_color_bgr[1] + tolerance), min(255, target_color_bgr[2] + tolerance)])

    color_mask = cv2.inRange(image_np, lower_bound, upper_bound)

    background_mask = cv2.inRange(image_np, (0, 0, 0), (254, 254, 254))

    final_mask = cv2.bitwise_and(color_mask, background_mask)

    total_pixels = image_np.size / 3  # Divide by 3 because image.size gives total number of channels
    target_pixels = np.sum(final_mask > 0)
    percentage = (target_pixels / total_pixels) * 100

    print(f"Percentage of target color in the image: {percentage:.2f}%")
    if percentage > threshold_percentage:
        print("The target color is present in more than 30% of the image.")
    else:
        print("The target color is not present in more than 30% of the image.")

# Instead of displaying the result, print the color percentage
if result:
    check_color_presence(result, (0,0,0), 30)  # Example: checking for red color presence with a threshold of 10%


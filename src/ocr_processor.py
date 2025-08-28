import easyocr
import cv2
import numpy as np
from PIL import Image
import io

# For the first run, the model will be downloaded automatically.
# This Reader should only be initialized once to keep it in memory.
try:
    # Using gpu=False to ensure compatibility on systems without a dedicated GPU.
    reader = easyocr.Reader(['fa', 'en'], gpu=False)
    print("EasyOCR reader loaded successfully.")
except Exception as e:
    print(f"Error loading EasyOCR reader: {e}")
    reader = None

def group_text_into_lines(results, y_tolerance=10):
    """
    Groups OCR results into lines based on the vertical position of their bounding boxes.
    
    Args:
        results (list): The raw output from EasyOCR.
        y_tolerance (int): The maximum vertical distance between the centers of two
                           bounding boxes to be considered on the same line.

    Returns:
        str: The formatted text with reconstructed lines.
    """
    if not results:
        return ""

    lines = []
    current_line = []
    
    # Sort results by their top y-coordinate to process them in reading order
    results.sort(key=lambda r: r[0][0][1]) 

    for bbox, text, prob in results:
        # Calculate the vertical center of the current bounding box
        y_center = (bbox[0][1] + bbox[2][1]) / 2
        
        if not current_line:
            current_line.append((bbox, text, y_center))
        else:
            # Get the average y_center of the current line
            avg_line_y = sum(item[2] for item in current_line) / len(current_line)
            
            # Check if the new box is vertically close enough to the current line
            if abs(y_center - avg_line_y) < y_tolerance:
                current_line.append((bbox, text, y_center))
            else:
                # If it's a new line, process the previous one and start a new one
                lines.append(current_line)
                current_line = [(bbox, text, y_center)]
    
    # Add the last line
    if current_line:
        lines.append(current_line)

    # Sort words within each line by their horizontal position (x-coordinate)
    # and join them into a final string
    final_text = []
    for line in lines:
        # --- CHANGE: Sort in reverse for right-to-left languages ---
        # Sort by the top-left x-coordinate in descending order (right to left)
        line.sort(key=lambda item: item[0][0][0], reverse=True) 
        line_text = " ".join([item[1] for item in line])
        final_text.append(line_text)
        
    return "\n".join(final_text)


def process_image(image_bytes):
    """
    This function takes an image as bytes, extracts Persian/English text,
    draws bounding boxes, and returns the processed image and reconstructed text.
    """
    if reader is None:
        raise RuntimeError("EasyOCR reader could not be initialized.")

    try:
        # Convert image bytes to a format that OpenCV can read
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform OCR on the image
        results = reader.readtext(img_cv)

        # Draw bounding boxes on the image
        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(img_cv, top_left, bottom_right, (0, 255, 0), 2)
            
        # Convert the processed OpenCV image (BGR) to a PIL image (RGB) for display
        processed_image_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        
        # Use the updated function to group text into lines
        full_text = group_text_into_lines(results)
        
        return processed_image_pil, full_text

    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        # On error, return the original image and an error message
        original_image = Image.open(io.BytesIO(image_bytes))
        return original_image, f"Error during processing: {e}"


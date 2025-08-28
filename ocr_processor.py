import easyocr
import cv2
import numpy as np
from PIL import Image

try:
    reader = easyocr.Reader(['fa', 'en'], gpu=False)
    print("EasyOCR reader loaded successfully.")
except Exception as e:
    print(f"Error loading EasyOCR reader: {e}")
    reader = None

def process_image(image_bytes):
    if reader is None:
        raise RuntimeError("EasyOCR reader could not be initialized.")

    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = reader.readtext(img_cv)

        extracted_texts = []
        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            
            cv2.rectangle(img_cv, top_left, bottom_right, (0, 255, 0), 2)
            
            extracted_texts.append(text)
            
        processed_image_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        
        full_text = "\n".join(extracted_texts)
        
        return processed_image_pil, full_text

    except Exception as e:
        print(f"An error occurred during image processing: {e}")
        # در صورت بروز خطا، تصویر اصلی و یک پیام خطا را برمی‌گردانیم
        original_image = Image.open(io.BytesIO(image_bytes))
        return original_image, f"[Error] Processing image failed. {e}"

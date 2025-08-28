import gradio as gr
from PIL import Image
import io
from src.ocr_processor import process_image # Assuming ocr_processor.py is in the same directory

def ocr_interface(input_image):
    """
    A wrapper function to connect Gradio's PIL Image input
    to our byte-based process_image function.
    """
    if input_image is None:
        # Return empty outputs if no image is provided
        return None, "Please upload an image first."

    # Convert the input PIL Image to bytes
    with io.BytesIO() as output_byte_stream:
        # Save the image in PNG format to the byte stream
        input_image.save(output_byte_stream, format="PNG")
        image_bytes = output_byte_stream.getvalue()

    try:
        # Call the processing function from ocr_processor.py
        processed_image, extracted_text = process_image(image_bytes)
        print(extracted_text)
        
        # Provide a default message if no text is found
        if not extracted_text:
            extracted_text = "No text could be detected in the image."
            
        return processed_image, extracted_text
    except Exception as e:
        # Return the original image on error to avoid crashing the UI
        return input_image, f"An unexpected error occurred: {e}"

# --- Build the Gradio Interface using Blocks for a custom layout ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Persian & English OCR: Extract Text from Images 📝")
    gr.Markdown("This tool uses the `EasyOCR` library to extract Persian and English text from your images.")

    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload an Image (JPG, PNG)")
            submit_button = gr.Button("Extract Text", variant="primary")

        with gr.Column(scale=2):
            image_output = gr.Image(label="Processed Image")
            
            # --- Section for Full Text Display and Copy ---
            with gr.Column():
                # --- CHANGE: Set textbox to display multiple lines ---
                text_output = gr.Textbox(label="Extracted Text", lines=10, interactive=False)
                copy_button = gr.Button("📋 Copy Full Text")

    # --- Define the interaction for the main submit button ---
    submit_button.click(
        fn=ocr_interface,
        inputs=image_input,
        outputs=[image_output, text_output],
        api_name="ocr" # You can call this API endpoint
    )

    # --- Define the interaction for the copy button ---
    copy_button.click(
        fn=None, 
        inputs=text_output,
        outputs=None,
        js="(text) => { navigator.clipboard.writeText(text) }"
    ).then(
        fn=lambda: gr.Info("Text copied to clipboard!"),
        inputs=None,
        outputs=None
    )

    gr.Markdown(
        """
        ---
        Created by **[Your Name]** | This is a Gradio implementation of the OCR tool.
        """
    )

# --- Launch the app ---
if __name__ == "__main__":
    demo.launch()


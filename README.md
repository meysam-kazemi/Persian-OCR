# 🤖 Persian OCR with Intelligent Line Reconstruction

A web-based tool built with Gradio and EasyOCR that extracts Persian and English text from images. This project features an advanced algorithm to accurately reconstruct text lines and handle right-to-left (RTL) word order, preserving the original layout of the document.

---

### 🖼️ Project Demo

![Demo GIF](https://github.com/meysam-kazemi/Persian-OCR/blob/main/assets/output.png)

---

### ✨ Key Features

-   **Intelligent Line Reconstruction:** Uses bounding box coordinates to intelligently group words into lines, preserving the original text layout instead of just listing words.
-   **Right-to-Left (RTL) Support:** Correctly orders words within each line from right to left, ensuring accurate Persian text output.
-   **Simple Web Interface:** An easy-to-use and clean UI built with Gradio for uploading images and viewing results.
-   **Visual Feedback:** Displays the processed image with green bounding boxes drawn around all detected text for easy verification.

---

### 🛠️ Technologies Used

-   Python
-   Gradio
-   EasyOCR
-   OpenCV, Pillow

---

### 🚀 How to Run Locally

Follow these steps to set up and run the project on your local machine.

**1. Clone the Repository:**
```bash
git clone https://github.com/meysam-kazemi/Persian-OCR.git
cd Persian-OCR
````

**2. Create and Activate a Virtual Environment:**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies:**
All required packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Run the Application:**

```bash
python app.py
```

A local URL (usually `http://127.0.0.1:7860`) will be displayed in your terminal. Open it in your web browser to use the application.

-----

### 📂 Project Structure

The project is organized into the following files and directories:

```
Persian-OCR/
├── src/
│   └── ocr_processor.py   # Core module for image processing, OCR, and text reconstruction.
├── app.py                 # The main Gradio application file that runs the web interface.
└── requirements.txt       # A list of all necessary Python packages.
```

-----

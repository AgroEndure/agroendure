import streamlit as st
import google.generativeai as genai
from pathlib import Path
import os

# --- MANUAL GOOGLE API KEY ---
GOOGLE_API_KEY = "AIzaSyBDul6jJbpOB0fkOXeAuzBawb_weCag4jE"  # 🔑 Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# --- USE A STABLE MODEL NAME ---
# "gemini-1.5-flash" may not work in all regions, so use gemini-1.0-pro for full compatibility
model = genai.GenerativeModel(model_name="gemini-1.0-pro")

# --- Function: Read image data ---
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

# --- Function: Generate AI response from image ---
def generate_gemini_response(prompt, image_path):
    image_data = read_image_data(image_path)
    response = model.generate_content([prompt, image_data])
    return response.text

# --- Prompt for Gemini ---
input_prompt = """
You are an expert plant pathologist.
Analyze the uploaded leaf image to identify any possible plant diseases.
1. Identify the disease name (if any).
2. Describe visible symptoms (color, spots, dryness, etc.).
3. Suggest an organic treatment using natural or home-based methods.
4. Give preventive advice for future crop safety.
Make the response easy to understand for farmers.
"""

# --- Streamlit UI ---
st.title("🌿 AgroEndure: Leaf Disease Detection AI")
st.write("Upload a clear photo of a leaf to detect diseases and get organic remedies.")

uploaded_file = st.file_uploader("📸 Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Save uploaded image temporarily
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Analyze the image
        with st.spinner("🧠 Analyzing leaf image... Please wait"):
            result = generate_gemini_response(input_prompt, file_path)

        # Display results
        st.image(file_path, caption="Uploaded Leaf", use_column_width=True)
        st.text_area("🧾 AI Disease Analysis & Recommendations", result, height=300)

        # Cleanup temp file
        os.remove(file_path)

    except Exception as e:
        st.error(f"❌ Error processing the image: {e}")


import streamlit as st
import google.generativeai as genai
from pathlib import Path
import os

# -------------------------------
# 🔑 Configure Google Gemini API
# -------------------------------
GOOGLE_API_KEY = "AIzaSyBDul6jJbpOB0fkOXeAuzBawb_weCag4jE"  # <-- Replace with your key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
# "gemini-1.5-flash" is fast and supports image input
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# 📸 Helper Function
# -------------------------------
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    # Google Gemini expects binary image data with a MIME type
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

# -------------------------------
# 🤖 AI Generation Function
# -------------------------------
def generate_gemini_response(prompt, image_path):
    try:
        image_data = read_image_data(image_path)
        response = model.generate_content([prompt, image_data])
        return response.text
    except Exception as e:
        return f"⚠️ Error generating response: {e}"

# -------------------------------
# 🧠 Plant Disease Prompt
# -------------------------------
input_prompt = """
You are an expert plant pathologist. Analyze the uploaded leaf image to identify potential plant diseases.

Provide the following details:
1. Disease Name and Type (fungal, bacterial, viral, or environmental).
2. Description of visible symptoms.
3. Probable Cause or Source.
4. Organic/Natural Remedies that farmers can apply.
5. Preventive Measures for future.
6. Any additional environmental or nutrient advice (e.g., pH level, water condition).

Keep your explanation simple, clear, and friendly for farmers.
End with: "⚠️ This is an AI-based analysis. Consult an agricultural expert for confirmation."
"""

# -------------------------------
# 🌿 Streamlit UI
# -------------------------------
st.set_page_config(page_title="Leaf Disease Detection | AgroEndure", layout="centered")
st.title("🌱 AgroEndure - Leaf Disease Detection")
st.write("Upload a leaf image below. The AI will identify possible diseases and suggest organic solutions.")

uploaded_file = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        # Save temporarily
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Show the uploaded image
        st.image(file_path, caption="🖼️ Uploaded Leaf Image", use_container_width=True)

        with st.spinner("Analyzing leaf... 🌿"):
            result = generate_gemini_response(input_prompt, file_path)

        st.success("✅ Analysis Complete!")
        st.text_area("AI Disease Analysis Report", result, height=350)

        # Clean up the temp file
        os.remove(file_path)

    except Exception as e:
        st.error(f"❌ Error processing the image: {e}")
else:
    st.info("📷 Please upload a leaf image to start the analysis.")


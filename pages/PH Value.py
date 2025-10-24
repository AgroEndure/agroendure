# streamlit_gpt5_ph.py
from openai import OpenAI
import streamlit as st
import os

# --- Configure API key (recommended: set OPENAI_API_KEY env variable) ---
# Example (Linux/macOS): export OPENAI_API_KEY="sk-..."
# Example (Windows PowerShell): $env:OPENAI_API_KEY="sk-..."
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-Iydn2O5va_WaSUr9gmpDqQHTg428xBBUBlr_R0g1zM-EzyqOiL4zLjqPhVHuKDNr848NRFY4bOT3BlbkFJe4EfTqx073tdLTl-3Yjy4EH2A8MFdBopQmFhIB5vUdZDN_s3rGcbxjYU3YF2hB43-XhYnh7toAsk-proj-Iydn2O5va_WaSUr9gmpDqQHTg428xBBUBlr_R0g1zM-EzyqOiL4zLjqPhVHuKDNr848NRFY4bOT3BlbkFJe4EfTqx073tdLTl-3Yjy4EH2A8MFdBopQmFhIB5vUdZDN_s3rGcbxjYU3YF2hB43-XhYnh7toA")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Function to get pH recommendation from GPT-5-style API ---
def get_ph_recommendation(ph_value: float) -> str:
    if ph_value < 7:
        prompt = (
            f"The water has a pH value of {ph_value}, which is acidic. "
            "Please recommend organic procedures or filter-based solutions to raise the pH level and neutralize the acidity. "
            "The goal is to bring the pH to 7 (neutral) without using chemicals. "
            "You can include filters, natural substances, or other organic methods. "
            "Give step-by-step, practical guidance suitable for a farmer or small-scale operator."
        )
    elif ph_value > 7:
        prompt = (
            f"The water has a pH value of {ph_value}, which is basic. "
            "Please recommend organic procedures or filter-based solutions to lower the pH level and neutralize the basicity. "
            "The goal is to bring the pH to 7 (neutral) without using chemicals. "
            "You can include filters, natural substances, or other organic methods. "
            "Give step-by-step, practical guidance suitable for a farmer or small-scale operator."
        )
    else:
        return "The water has a neutral pH of 7. No treatment is necessary."

    try:
        completion = client.chat.completions.create(
            model="gpt-5",                # Use gpt-5 (or the exact GPT-5 variant available to your account)
            messages=[
                {"role": "system", "content": "You are a helpful assistant for practical water treatment and farmer-friendly advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        # The new client returns a structure where the content is under choices[0].message.content
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- Streamlit interface ---
def streamlit_interface():
    st.title("Water pH Treatment Recommendation (GPT-5)")
    st.write("Enter the pH value of your water to get recommendations for neutralizing it using organic methods or filter-based solutions.")
    ph_value = st.number_input("Enter pH value", min_value=0.0, max_value=14.0, step=0.1, value=7.0)

    if st.button("Get Recommendation"):
        with st.spinner("Generating recommendation..."):
            recommendation = get_ph_recommendation(ph_value)
        st.text_area("Recommended Procedure", value=recommendation, height=260)

if __name__ == "__main__":
    streamlit_interface()


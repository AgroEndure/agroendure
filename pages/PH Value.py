import openai
import streamlit as st
import os

# Set OpenAI API key directly
OPENAI_API_KEY = "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"  # Replace with your actual API key
openai.api_key = OPENAI_API_KEY

# Function to get pH recommendation from OpenAI API
def get_ph_recommendation(ph_value):
    if ph_value < 7:
        prompt = f"""
        The water has a pH value of {ph_value}, which is acidic. 
        Please recommend organic procedures or filter-based solutions to raise the pH level and neutralize the acidity. 
        The goal is to bring the pH to 7 (neutral) without using chemicals. 
        You can include filters, natural substances, or other organic methods.
        """
    elif ph_value > 7:
        prompt = f"""
        The water has a pH value of {ph_value}, which is basic.
        Please recommend organic procedures or filter-based solutions to lower the pH level and neutralize the basicity.
        The goal is to bring the pH to 7 (neutral) without using chemicals.
        You can include filters, natural substances, or other organic methods.
        """
    else:
        return "The water has a neutral pH of 7. No treatment is necessary."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for water treatment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit interface
def streamlit_interface():
    st.title("Water pH Treatment Recommendation")
    st.write("Enter the pH value of your water to get recommendations for neutralizing it using organic methods or filter-based solutions.")
    ph_value = st.number_input("Enter pH value", min_value=0.0, max_value=14.0, step=0.1)
    if ph_value:
        recommendation = get_ph_recommendation(ph_value)
        st.text_area("Recommended Procedure", value=recommendation, height=150)

if __name__ == "__main__":
    streamlit_interface()

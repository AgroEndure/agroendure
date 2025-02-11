import streamlit as st
import pandas as pd
import openai
import os
import re

# Set OpenAI API key directly
OPENAI_API_KEY = "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"  # Replace with your actual API key
openai.api_key = OPENAI_API_KEY

# Function to fetch ideal NPK values for a crop using OpenAI
def fetch_ideal_npk(crop):
    prompt = f"""
    Provide the ideal Nitrogen (N), Phosphorus (P), and Potassium (K) values for optimal growth of {crop}.
    Respond ONLY in the format: N: <value>, P: <value>, K: <value> (numbers only, no text)
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert agronomist providing ideal soil nutrient values for crops."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        content = response['choices'][0]['message']['content'].strip()
        values = re.findall(r'\d+', content)
        if len(values) == 3:
            return {"N": int(values[0]), "P": int(values[1]), "K": int(values[2])}
        else:
            return f"Error: Unexpected format received from OpenAI. Response: {content}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to load NPK values from dummydata.csv
def load_npk_from_csv(file_path="dummydata.csv"):
    data = pd.read_csv(file_path, header=None)
    nitrogen, phosphorus, potassium = data.iloc[0].values[:3]
    return nitrogen, phosphorus, potassium

# Function to compare NPK values and suggest improvements
def analyze_soil_npk(crop):
    nitrogen, phosphorus, potassium = load_npk_from_csv()
    ideal_npk = fetch_ideal_npk(crop)
    
    if isinstance(ideal_npk, str):
        return ideal_npk  
    
    recommendations = []
    if nitrogen < ideal_npk['N']:
        recommendations.append(f"Increase Nitrogen (N). Ideal: {ideal_npk['N']}, Current: {nitrogen}")
    if phosphorus < ideal_npk['P']:
        recommendations.append(f"Increase Phosphorus (P). Ideal: {ideal_npk['P']}, Current: {phosphorus}")
    if potassium < ideal_npk['K']:
        recommendations.append(f"Increase Potassium (K). Ideal: {ideal_npk['K']}, Current: {potassium}")
    
    if not recommendations:
        return "The soil has ideal NPK levels for this crop. No adjustments needed."
    
    organic_recommendations = get_organic_amendments(recommendations)
    return f"### Soil Analysis:\n" + "\n".join(recommendations) + "\n\n### Organic Amendments:\n" + organic_recommendations

# Function to get organic amendments using OpenAI
def get_organic_amendments(recommendations):
    prompt = f"""
    Given the following soil deficiencies:
    {', '.join(recommendations)}
    Suggest natural organic materials or methods to improve the soil fertility without chemicals.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert agronomist helping farmers improve soil health."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("\U0001F331 Soil Nutrient Analysis")
st.write("Enter the crop name to analyze soil NPK levels and get organic amendment suggestions.")

# User input
crop_name = st.text_input("Enter Crop Name")

if st.button("Analyze Soil"):
    if crop_name:
        with st.spinner("Analyzing soil..."):
            result = analyze_soil_npk(crop_name)
        st.markdown(result)
    else:
        st.warning("Please enter a crop name.")

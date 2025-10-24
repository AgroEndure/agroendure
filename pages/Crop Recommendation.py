import streamlit as st
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily

# --- Load dummydata.csv ---
def load_data_from_csv(file_path="dummydata.csv"):
    data = pd.read_csv(file_path, header=None)
    nitrogen, phosphorus, potassium, ph_value, moisture = data.iloc[0].values
    return nitrogen, phosphorus, potassium, ph_value, moisture

# --- Streamlit UI ---
st.title("🌾 AgroEndure: Smart Crop & Soil Recommendation System")

st.header("📊 Crop Recommendation Based on Soil & Weather")

# Button to update values
def update_values_from_csv():
    nitrogen, phosphorus, potassium, ph_value, moisture = load_data_from_csv()
    st.session_state.n_value = nitrogen
    st.session_state.p_value = phosphorus
    st.session_state.k_value = potassium
    st.session_state.ph_value = ph_value
    st.session_state.moisture = moisture

if st.button("🔄 Load Latest Data from CSV"):
    update_values_from_csv()
    st.success("✅ Latest data loaded successfully!")

# Display inputs
n_value = st.number_input("Nitrogen (N)", value=st.session_state.get("n_value", 5.2))
p_value = st.number_input("Phosphorus (P)", value=st.session_state.get("p_value", 3.1))
k_value = st.number_input("Potassium (K)", value=st.session_state.get("k_value", 6.7))
ph_value = st.number_input("pH Value", value=st.session_state.get("ph_value", 6.5))

target_year = st.text_input("Target Year", "2023")
start_month = st.text_input("Start Month", "1")
start_day = st.text_input("Start Day", "1")
end_month = st.text_input("End Month", "12")
end_day = st.text_input("End Day", "31")

# --- Manual Crop Recommendation Logic ---
def get_manual_crop_recommendation(n, p, k, ph):
    if ph < 6:
        soil_type = "acidic"
    elif ph > 7.5:
        soil_type = "alkaline"
    else:
        soil_type = "neutral"

    if n < 4 and p < 4 and k < 4:
        return f"🪴 The soil is low in all nutrients and {soil_type}. Ideal crops: **Pulses, Groundnut, and Peas** — they fix nitrogen and improve soil fertility."
    elif n > 7 and p > 7 and k > 7:
        return f"🌽 The soil is highly fertile and {soil_type}. Best crops: **Maize, Sugarcane, Cotton, and Wheat** — they thrive in rich, balanced soil."
    elif n > 7 and p < 5:
        return f"🌿 The soil has high nitrogen but low phosphorus — good for **Leafy Vegetables (Spinach, Lettuce)** but add organic compost or bone meal to improve root growth."
    elif k < 4:
        return f"🥔 The soil is low in potassium — suitable for crops like **Potatoes, Tomatoes, and Bananas** with added wood ash or compost to boost K levels."
    elif p > 7 and k > 7:
        return f"🌾 High phosphorus and potassium — great for **Rice, Wheat, and Barley**, ensuring strong roots and grain yield."
    else:
        return f"🌱 Balanced soil with {soil_type} nature — suitable for **Tomatoes, Chilies, Beans, and Sunflower**."

# --- Weather Data Fetch ---
def get_weather_data(target_year, start_month, start_day, end_month, end_day):
    lahore = Point(31.5497, 74.3436, 217)

    target_year = int(target_year)
    start_month = int(start_month)
    start_day = int(start_day)
    end_month = int(end_month)
    end_day = int(end_day)

    start = datetime(target_year, start_month, start_day)
    end = datetime(target_year, end_month, end_day)

    data = Daily(lahore, start, end)
    data = data.fetch()

    averages = {}
    if 'tavg' in data.columns:
        averages['tavg'] = round(data['tavg'].mean(), 2)
    if 'prcp' in data.columns:
        averages['prcp'] = round(data['prcp'].mean(), 2)
    if 'rhum' in data.columns:
        averages['rhum'] = round(data['rhum'].mean(), 2)

    return averages

# --- Combine Weather & Crop Recommendation ---
def combined_recommendation(n, p, k, ph, target_year, start_month, start_day, end_month, end_day):
    crop_suggestion = get_manual_crop_recommendation(n, p, k, ph)
    weather_data = get_weather_data(target_year, start_month, start_day, end_month, end_day)

    weather_info = f"""
**🌦️ Historical Weather Data:**
- Avg Temperature: {weather_data.get('tavg', 'N/A')} °C
- Avg Rainfall: {weather_data.get('prcp', 'N/A')} mm
- Avg Humidity: {weather_data.get('rhum', 'N/A')} %
    """

    return f"{crop_suggestion}\n\n{weather_info}"

# --- Button to Show Recommendations ---
if st.button("🌾 Get Recommendations"):
    with st.spinner("Analyzing soil and weather..."):
        final_recommendation = combined_recommendation(
            n_value, p_value, k_value, ph_value,
            target_year, start_month, start_day, end_month, end_day
        )
    st.success("✅ Recommendation Generated!")
    st.text_area("Result", value=final_recommendation, height=280)

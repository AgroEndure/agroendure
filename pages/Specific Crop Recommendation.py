import streamlit as st
import pandas as pd

# --- Load NPK values from dummydata.csv ---
def load_npk_from_csv(file_path="dummydata.csv"):
    data = pd.read_csv(file_path, header=None)
    nitrogen, phosphorus, potassium = data.iloc[0].values[:3]
    return nitrogen, phosphorus, potassium

# --- Manual database of ideal NPK values (example crops) ---
IDEAL_NPK_VALUES = {
    "wheat": {"N": 6, "P": 5, "K": 5},
    "rice": {"N": 7, "P": 6, "K": 6},
    "maize": {"N": 8, "P": 6, "K": 7},
    "cotton": {"N": 7, "P": 5, "K": 8},
    "sugarcane": {"N": 9, "P": 6, "K": 8},
    "tomato": {"N": 7, "P": 6, "K": 7},
    "potato": {"N": 8, "P": 5, "K": 9},
    "soybean": {"N": 5, "P": 6, "K": 5},
    "sunflower": {"N": 6, "P": 5, "K": 7},
    "chili": {"N": 6, "P": 6, "K": 6},
}

# --- Manual organic recommendations based on deficiencies ---
def organic_amendment_suggestions(nitrogen_low, phosphorus_low, potassium_low):
    tips = []
    if nitrogen_low:
        tips.append("🌿 **To increase Nitrogen (N):** Use composted manure, green leaves, legume crops (peas, beans), or cow dung slurry.")
    if phosphorus_low:
        tips.append("🌾 **To increase Phosphorus (P):** Add bone meal, rock phosphate, banana peels, or poultry manure.")
    if potassium_low:
        tips.append("🥔 **To increase Potassium (K):** Use wood ash, banana stems, sugarcane bagasse compost, or coconut coir compost.")
    if not tips:
        tips.append("✅ The soil already has balanced nutrient levels — keep maintaining with regular organic compost.")
    return "\n".join(tips)

# --- Main Soil NPK Analysis Function ---
def analyze_soil_npk(crop):
    crop = crop.lower().strip()
    nitrogen, phosphorus, potassium = load_npk_from_csv()

    if crop not in IDEAL_NPK_VALUES:
        return f"⚠️ Sorry, data for '{crop}' is not available. Try one of: {', '.join(IDEAL_NPK_VALUES.keys())}"

    ideal_npk = IDEAL_NPK_VALUES[crop]
    recommendations = []

    nitrogen_low = nitrogen < ideal_npk['N']
    phosphorus_low = phosphorus < ideal_npk['P']
    potassium_low = potassium < ideal_npk['K']

    if nitrogen_low:
        recommendations.append(f"🔸 Increase Nitrogen (N): Ideal {ideal_npk['N']}, Current {nitrogen}")
    if phosphorus_low:
        recommendations.append(f"🔸 Increase Phosphorus (P): Ideal {ideal_npk['P']}, Current {phosphorus}")
    if potassium_low:
        recommendations.append(f"🔸 Increase Potassium (K): Ideal {ideal_npk['K']}, Current {potassium}")

    if not recommendations:
        result = "✅ The soil has ideal NPK levels for this crop. No adjustments needed."
    else:
        result = "### Soil Analysis:\n" + "\n".join(recommendations)

    organic_solutions = organic_amendment_suggestions(nitrogen_low, phosphorus_low, potassium_low)
    return f"{result}\n\n### 🌱 Organic Recommendations:\n{organic_solutions}"

# --- Streamlit UI ---
st.title("🌾 AgroEndure: Soil Nutrient & Organic Fertility Analysis")
st.write("Enter the crop name to analyze soil NPK levels and get **organic improvement suggestions** (works fully offline).")

# User input
crop_name = st.text_input("Enter Crop Name (e.g., Wheat, Rice, Tomato)")

if st.button("🔍 Analyze Soil"):
    if crop_name:
        with st.spinner("Analyzing soil composition..."):
            result = analyze_soil_npk(crop_name)
        st.markdown(result)
    else:
        st.warning("⚠️ Please enter a crop name first.")

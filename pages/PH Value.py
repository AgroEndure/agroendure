# streamlit_ph_manual.py
import streamlit as st

# --- Function to get pH recommendation manually ---
def get_ph_recommendation(ph_value: float) -> str:
    if ph_value < 7:
        return (
            f"The water has a pH value of {ph_value}, which is acidic.\n\n"
            "✅ **Organic Recommendations to Raise pH (Reduce Acidity):**\n"
            "- Use crushed limestone or dolomite in small amounts — these are natural and safe buffers.\n"
            "- Add a layer of **biochar** (organic charcoal) to your filtration tank — it helps neutralize acidity.\n"
            "- Mix in **wood ash** (moderately) if the water is used for crops — it naturally increases pH.\n"
            "- Pass water through a **gravel and coral sand filter** to balance the acidity.\n"
            "- Regularly check pH and stop treatment once it reaches near 7.\n\n"
            "💧 *Goal:* Gradually move toward a neutral pH without using synthetic chemicals."
        )

    elif ph_value > 7:
        return (
            f"The water has a pH value of {ph_value}, which is basic (alkaline).\n\n"
            "✅ **Organic Recommendations to Lower pH (Reduce Alkalinity):**\n"
            "- Add **peat moss** or **compost tea** into your filtration setup — these naturally release mild acids.\n"
            "- Pass water through a **coconut shell activated carbon filter** — helps neutralize alkalinity.\n"
            "- Add small quantities of **lemon juice or vinegar** (for domestic use only, not irrigation).\n"
            "- Use **sulfur-coated sand filters** or **rice husk biofilters** — they gradually balance pH.\n"
            "- Monitor weekly until pH reaches around 7.\n\n"
            "💧 *Goal:* Neutralize the basicity gently without any harsh chemicals."
        )

    else:
        return (
            f"The water has a neutral pH of {ph_value}. ✅\n\n"
            "No treatment is required.\n"
            "Keep monitoring pH monthly to ensure it stays stable, especially if your water source changes."
        )

# --- Streamlit interface ---
def streamlit_interface():
    st.title("Water pH Treatment Recommendation (Offline Version)")
    st.write("Enter the pH value of your water to get predefined organic recommendations — no internet or API key required.")

    ph_value = st.number_input("Enter pH value", min_value=0.0, max_value=14.0, step=0.1, value=7.0)

    if st.button("Get Recommendation"):
        recommendation = get_ph_recommendation(ph_value)
        st.text_area("Recommended Procedure", value=recommendation, height=300)

if __name__ == "__main__":
    streamlit_interface()

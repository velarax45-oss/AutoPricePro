# ============================================================
# AutoPricePro — Streamlit Web App
# Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ============================================================
# Page Config
# ============================================================
st.set_page_config(
    page_title="AutoPricePro",
    page_icon="🚗",
    layout="centered"
)

# ============================================================
# Custom CSS — clean dark card UI
# ============================================================
st.markdown("""
<style>
    /* Background */
    .stApp { background-color: #0f1117; color: #f0f0f0; }

    /* Title block */
    .title-block {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
    }
    .title-block h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f97316, #facc15);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .title-block p {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0;
    }

    /* Card */
    .card {
        background: #1e2130;
        border: 1px solid #2d3148;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }

    /* Section header */
    .section-header {
        color: #f97316;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
    }

    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #1a2540, #0f172a);
        border: 1px solid #f97316;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-box .label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .result-box .price {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f97316, #facc15);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .result-box .range {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* Selectbox & slider labels */
    label { color: #cbd5e1 !important; font-size: 0.9rem !important; }

    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #f97316, #facc15);
        color: #0f1117;
        font-weight: 800;
        font-size: 1.1rem;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        margin-top: 1rem;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load Artifacts
# ============================================================
@st.cache_resource
def load_artifacts():
    model          = joblib.load("AutoPricePro.pkl")
    brand_model_map = joblib.load("brand_model_map.pkl")
    meta           = joblib.load("meta.pkl")
    return model, brand_model_map, meta

try:
    model, brand_model_map, meta = load_artifacts()
except FileNotFoundError as e:
    st.error(f"❌ Missing file: {e}\nPlease run **train_model.py** first.")
    st.stop()

# ============================================================
# Title
# ============================================================
st.markdown("""
<div class="title-block">
    <h1>🚗 AutoPricePro</h1>
    <p>AI-Powered Used Car Valuation Engine</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Form
# ============================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🚘 Car Identity</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    brands = sorted(brand_model_map.keys())
    selected_brand = st.selectbox("Select Brand", brands)

with col2:
    models_for_brand = brand_model_map.get(selected_brand, [])
    # Safety: filter out any NaN-like values
    models_for_brand = [
        m for m in models_for_brand
        if m and str(m).strip().lower() not in ("nan", "none", "")
    ]
    if not models_for_brand:
        models_for_brand = ["Unknown"]
    selected_model = st.selectbox("Select Model", models_for_brand)

st.markdown('</div>', unsafe_allow_html=True)

# ---- Condition ----
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Car Condition</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    selected_year = st.slider(
        "Year of Manufacture",
        min_value=meta["year_min"],
        max_value=meta["year_max"],
        value=2018
    )

with col4:
    selected_km = st.slider(
        "KM Driven",
        min_value=meta["km_min"],
        max_value=meta["km_max"],
        value=50000,
        step=1000,
        format="%d km"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---- Specs ----
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">⚙️ Specifications</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    selected_fuel = st.selectbox("Fuel Type", meta["fuel_types"])
    selected_transmission = st.selectbox("Transmission", meta["transmission_types"])

with col6:
    selected_seller = st.selectbox("Seller Type", meta["seller_types"])
    selected_owner = st.selectbox("Owner", meta["owner_types"])

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Predict Button
# ============================================================
predict_clicked = st.button("🔍 Estimate Price")

if predict_clicked:
    # --- Validate model string ---
    selected_model_str = str(selected_model).strip()
    if selected_model_str.lower() in ("nan", "none", ""):
        st.error("⚠️ Please select a valid car model.")
        st.stop()

    # --- Build full name ---
    full_name = f"{selected_brand} {selected_model_str}"   # safe — both are clean str

    # --- Derived features ---
    age    = 2026 - selected_year
    km_log = np.log1p(selected_km)

    # --- Input DataFrame ---
    input_df = pd.DataFrame([{
        "brand"       : selected_brand,
        "model"       : selected_model_str,
        "age"         : age,
        "km_log"      : km_log,
        "fuel"        : selected_fuel,
        "seller_type" : selected_seller,
        "transmission": selected_transmission,
        "owner"       : selected_owner,
    }])

    # --- Predict ---
    try:
        predicted_price = model.predict(input_df)[0]

        # Confidence range: ±8%
        low  = predicted_price * 0.92
        high = predicted_price * 1.08

        def fmt(v):
            if v >= 1_00_000:
                return f"₹{v/1_00_000:.2f} L"
            return f"₹{v:,.0f}"

        st.markdown(f"""
        <div class="result-box">
            <div class="label">Estimated Market Value</div>
            <div class="price">{fmt(predicted_price)}</div>
            <div class="range">Likely range: {fmt(low)} — {fmt(high)}</div>
            <br>
            <div style="color:#64748b; font-size:0.8rem;">
                {full_name} · {selected_year} · {selected_km:,} km · {selected_fuel} · {selected_transmission}
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        st.stop()

# ============================================================
# Footer
# ============================================================
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.78rem; margin-top:3rem;">
    AutoPricePro · Powered by XGBoost · For estimation purposes only
</div>
""", unsafe_allow_html=True)

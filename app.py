import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
 
# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AutoPricePro",
    page_icon="🚗",
    layout="wide",
)
 
# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
 
html, body, [class*="css"] {
    background: #0d0f14;
    color: #e8eaf0;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 { font-family: 'Orbitron', sans-serif; }
 
/* Card */
.card {
    background: linear-gradient(135deg, #161b27 0%, #1a2035 100%);
    border: 1px solid #2a3a5c;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
 
/* Price badge */
.price-badge {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    border-radius: 14px;
    padding: 20px 30px;
    text-align: center;
    margin: 12px 0;
}
.price-badge .label { font-size: 13px; color: #93c5fd; letter-spacing: 2px; text-transform: uppercase; }
.price-badge .amount { font-size: 42px; font-weight: 700; font-family: 'Orbitron', sans-serif; color: #fff; }
.price-badge .range { font-size: 13px; color: #bfdbfe; margin-top: 4px; }
 
/* Metric pill */
.metric-pill {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
}
.metric-pill .m-label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
.metric-pill .m-value { font-size: 20px; font-weight: 700; color: #38bdf8; }
 
/* Tab styling */
[data-baseweb="tab"] { font-family: 'Orbitron', sans-serif; font-size: 13px; }
 
/* Divider */
.divider { border-top: 1px solid #2a3a5c; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
#  LOAD ARTIFACTS
# ─────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model       = joblib.load("AutoPricePro.pkl")
    brand_model = joblib.load("brand_model_map.pkl")
    meta        = joblib.load("meta.pkl")
    return model, brand_model, meta
 
model, brand_model_map, meta = load_artifacts()
 
# ✅ FIXED KEY NAMES — matches train_model.py exactly
fuels         = meta["fuel_types"]
transmissions = meta["transmission_types"]
seller_types  = meta["seller_types"]
owners        = meta["owner_types"]
year_min      = meta["year_min"]
year_max      = meta["year_max"]
km_max        = meta["km_max"]
brands        = sorted(brand_model_map.keys())
 
# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def build_input(brand, mdl, year, km, fuel, transmission, seller_type, owner):
    age    = 2026 - year
    km_log = np.log1p(km)
    return pd.DataFrame([{
        "brand":        brand,
        "model":        mdl,
        "age":          age,
        "km_log":       km_log,
        "fuel":         fuel,
        "seller_type":  seller_type,
        "transmission": transmission,
        "owner":        owner,
    }])
 
def predict_price(df_row):
    return max(model.predict(df_row)[0], 0)
 
def fmt_inr(val):
    lakh = val / 1e5
    if lakh >= 100:
        return f"₹{lakh/100:.2f} Cr"
    return f"₹{lakh:.2f} L"
 
def depreciation_series(brand, mdl, base_year, km, fuel, transmission, seller_type, owner):
    years, prices = [], []
    for yr in range(base_year, 2027):
        km_est = km * (yr - base_year + 1) / max((2026 - base_year), 1)
        row = build_input(brand, mdl, yr, km_est, fuel, transmission, seller_type, owner)
        price = predict_price(row)
        years.append(yr)
        prices.append(price)
    return years, prices
 
# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 32px 0 8px 0;">
  <h1 style="font-size:2.4rem; margin:0; background: linear-gradient(90deg,#38bdf8,#818cf8);
      -webkit-background-clip:text; -webkit-text-fill-color:transparent;">🚗 AutoPricePro</h1>
  <p style="color:#64748b; font-size:14px; margin-top:6px; letter-spacing:2px;">
      AI POWERED USED CAR VALUATION ENGINE
  </p>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍  Single Valuation", "🆚  Compare Two Cars"])
 
# ═══════════════════════════════════════════════
#  TAB 1 — SINGLE VALUATION
# ═══════════════════════════════════════════════
with tab1:
    col_form, col_result = st.columns([1, 1.2], gap="large")
 
    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### Enter Car Details")
 
        sel_brand   = st.selectbox("Brand", brands, key="s_brand")
        models_list = brand_model_map.get(sel_brand, [])
        sel_model   = st.selectbox("Model", models_list, key="s_model")
 
        c1, c2 = st.columns(2)
        with c1:
            sel_year = st.slider("Year", year_min, year_max, 2018, key="s_year")
        with c2:
            sel_km = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key="s_km")
 
        c3, c4 = st.columns(2)
        with c3:
            sel_fuel  = st.selectbox("Fuel", fuels, key="s_fuel")
        with c4:
            sel_trans = st.selectbox("Transmission", transmissions, key="s_trans")
 
        c5, c6 = st.columns(2)
        with c5:
            sel_seller = st.selectbox("Seller Type", seller_types, key="s_seller")
        with c6:
            sel_owner = st.selectbox("Owner", owners, key="s_owner")
 
        predict_btn = st.button("🔮 Predict Price", use_container_width=True, key="s_btn")
        st.markdown('</div>', unsafe_allow_html=True)
 
    with col_result:
        if predict_btn:
            row   = build_input(sel_brand, sel_model, sel_year, sel_km,
                                sel_fuel, sel_trans, sel_seller, sel_owner)
            price = predict_price(row)
            low, high = price * 0.92, price * 1.08
 
            st.markdown(f"""
            <div class="price-badge">
              <div class="label">Estimated Market Value</div>
              <div class="amount">{fmt_inr(price)}</div>
              <div class="range">Range: {fmt_inr(low)} – {fmt_inr(high)}</div>
            </div>
            """, unsafe_allow_html=True)
 
            age = 2026 - sel_year
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-pill"><div class="m-label">Age</div><div class="m-value">{age} yrs</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-pill"><div class="m-label">KM Driven</div><div class="m-value">{sel_km:,}</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-pill"><div class="m-label">Fuel</div><div class="m-value">{sel_fuel}</div></div>', unsafe_allow_html=True)
 
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
            # ── CHART 1: Depreciation Curve ──
            st.markdown("##### 📉 Depreciation Curve")
            yrs, prices = depreciation_series(
                sel_brand, sel_model, max(sel_year, 2010),
                sel_km, sel_fuel, sel_trans, sel_seller, sel_owner
            )
            fig_dep = go.Figure()
            fig_dep.add_trace(go.Scatter(
                x=yrs, y=[p/1e5 for p in prices],
                mode="lines+markers",
                line=dict(color="#38bdf8", width=3),
                marker=dict(size=6, color="#818cf8"),
                fill="tozeroy",
                fillcolor="rgba(56,189,248,0.08)",
                name="Value (₹ Lakh)"
            ))
            fig_dep.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis=dict(title="Year", gridcolor="#1e293b", showgrid=True),
                yaxis=dict(title="₹ Lakh", gridcolor="#1e293b", showgrid=True),
                margin=dict(l=0, r=0, t=10, b=0),
                height=230,
            )
            st.plotly_chart(fig_dep, use_container_width=True)
 
            # ── CHART 2: Price vs KM Driven ──
            st.markdown("##### 📈 Price vs KM Driven")
            km_range  = list(range(0, km_max + 1, 10000))
            prices_km = []
            for km_val in km_range:
                r = build_input(sel_brand, sel_model, sel_year, km_val,
                                sel_fuel, sel_trans, sel_seller, sel_owner)
                prices_km.append(predict_price(r) / 1e5)
 
            fig_km = go.Figure()
            fig_km.add_trace(go.Scatter(
                x=km_range, y=prices_km,
                mode="lines",
                line=dict(color="#818cf8", width=3),
                fill="tozeroy",
                fillcolor="rgba(129,140,248,0.08)",
            ))
            fig_km.add_vline(
                x=sel_km,
                line_dash="dash", line_color="#f59e0b",
                annotation_text=f"  Your KM: {sel_km:,}",
                annotation_font_color="#f59e0b",
            )
            fig_km.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis=dict(title="KM Driven", gridcolor="#1e293b", tickformat=","),
                yaxis=dict(title="₹ Lakh", gridcolor="#1e293b"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=230,
            )
            st.plotly_chart(fig_km, use_container_width=True)
 
        else:
            st.markdown("""
            <div style="text-align:center; padding:80px 20px; color:#334155;">
              <div style="font-size:64px;">🚗</div>
              <div style="font-size:16px; margin-top:12px;">Fill in the details and click<br>
              <b style="color:#38bdf8;">Predict Price</b></div>
            </div>
            """, unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════
#  TAB 2 — COMPARISON MODE
# ═══════════════════════════════════════════════
with tab2:
    st.markdown("#### 🆚 Compare Two Cars Side by Side")
 
    cc1, cc2 = st.columns(2, gap="large")
 
    def car_form(col, idx):
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            label = "Car A 🔵" if idx == 1 else "Car B 🟠"
            st.markdown(f"**{label}**")
            brand    = st.selectbox("Brand", brands, key=f"c{idx}_brand")
            mdl_list = brand_model_map.get(brand, [])
            mdl      = st.selectbox("Model", mdl_list, key=f"c{idx}_model")
            yr       = st.slider("Year", year_min, year_max, 2018 - (idx-1)*2, key=f"c{idx}_year")
            km       = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key=f"c{idx}_km")
            fuel     = st.selectbox("Fuel", fuels, key=f"c{idx}_fuel")
            trans    = st.selectbox("Transmission", transmissions, key=f"c{idx}_trans")
            seller   = st.selectbox("Seller Type", seller_types, key=f"c{idx}_seller")
            owner    = st.selectbox("Owner", owners, key=f"c{idx}_owner")
            st.markdown('</div>', unsafe_allow_html=True)
        return brand, mdl, yr, km, fuel, trans, seller, owner
 
    data_a = car_form(cc1, 1)
    data_b = car_form(cc2, 2)
 
    compare_btn = st.button("⚡ Compare Now", use_container_width=True)
 
    if compare_btn:
        brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a = data_a
        brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b = data_b
 
        row_a = build_input(brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a)
        row_b = build_input(brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b)
 
        price_a = predict_price(row_a)
        price_b = predict_price(row_b)
        winner  = "A 🔵" if price_a > price_b else "B 🟠"
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        r1, r2, r3 = st.columns([1, 0.3, 1])
        with r1:
            st.markdown(f"""
            <div class="price-badge" style="border:2px solid #38bdf8;">
              <div class="label">Car A — {brand_a} {mdl_a}</div>
              <div class="amount">{fmt_inr(price_a)}</div>
              <div class="range">{yr_a} · {km_a:,} km · {fuel_a}</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown('<div style="text-align:center;font-size:32px;padding-top:40px;color:#64748b;">VS</div>',
                        unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="price-badge" style="border:2px solid #f97316;">
              <div class="label">Car B — {brand_b} {mdl_b}</div>
              <div class="amount">{fmt_inr(price_b)}</div>
              <div class="range">{yr_b} · {km_b:,} km · {fuel_b}</div>
            </div>
            """, unsafe_allow_html=True)
 
        diff = abs(price_a - price_b)
        st.markdown(f"""
        <div style="text-align:center;padding:10px;color:#94a3b8;font-size:14px;">
            💡 Car <b>{winner}</b> has the higher estimated value &nbsp;|&nbsp;
            Difference: <b style="color:#f59e0b;">{fmt_inr(diff)}</b>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        ch1, ch2 = st.columns(2)
 
        with ch1:
            st.markdown("##### 📊 Price Comparison")
            fig_bar = go.Figure(go.Bar(
                x=[f"{brand_a} {mdl_a}", f"{brand_b} {mdl_b}"],
                y=[price_a / 1e5, price_b / 1e5],
                marker_color=["#38bdf8", "#f97316"],
                text=[fmt_inr(price_a), fmt_inr(price_b)],
                textposition="outside",
                textfont=dict(color="white"),
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                yaxis=dict(title="₹ Lakh", gridcolor="#1e293b"),
                xaxis=dict(gridcolor="#1e293b"),
                margin=dict(l=0, r=0, t=20, b=0),
                height=300,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
 
        with ch2:
            st.markdown("##### 📉 Depreciation Comparison")
            yrs_a, dep_a = depreciation_series(brand_a, mdl_a, max(yr_a, 2010), km_a, fuel_a, trans_a, seller_a, owner_a)
            yrs_b, dep_b = depreciation_series(brand_b, mdl_b, max(yr_b, 2010), km_b, fuel_b, trans_b, seller_b, owner_b)
 
            fig_dep2 = go.Figure()
            fig_dep2.add_trace(go.Scatter(
                x=yrs_a, y=[p/1e5 for p in dep_a],
                name=f"{brand_a} {mdl_a}",
                line=dict(color="#38bdf8", width=3),
            ))
            fig_dep2.add_trace(go.Scatter(
                x=yrs_b, y=[p/1e5 for p in dep_b],
                name=f"{brand_b} {mdl_b}",
                line=dict(color="#f97316", width=3),
            ))
            fig_dep2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                xaxis=dict(title="Year", gridcolor="#1e293b"),
                yaxis=dict(title="₹ Lakh", gridcolor="#1e293b"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
                margin=dict(l=0, r=0, t=20, b=0),
                height=300,
            )
            st.plotly_chart(fig_dep2, use_container_width=True)
 
        # ── Spec Table ──
        st.markdown("##### 📋 Specifications")
        specs_df = pd.DataFrame({
            "Specification": ["Brand", "Model", "Year", "KM Driven", "Fuel", "Transmission", "Seller", "Owner", "Est. Price"],
            f"Car A 🔵 {brand_a}": [brand_a, mdl_a, yr_a, f"{km_a:,} km", fuel_a, trans_a, seller_a, owner_a, fmt_inr(price_a)],
            f"Car B 🟠 {brand_b}": [brand_b, mdl_b, yr_b, f"{km_b:,} km", fuel_b, trans_b, seller_b, owner_b, fmt_inr(price_b)],
        })
        st.dataframe(specs_df.set_index("Specification"), use_container_width=True)
 
## ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 32px 0 8px 0; color:#334155; font-size:12px;">
    AutoPricePro · XGBoost · R² 95.46% · Built with Streamlit<br>
    <span style="color:#1e293b;">Predictions are estimates. Verify before transacting.</span>
</div>
""", unsafe_allow_html=True)
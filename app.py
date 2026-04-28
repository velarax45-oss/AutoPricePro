import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
 
# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AutoPricePro",
    page_icon="🚗",
    layout="wide",
)
 
# ─────────────────────────────────────────────
#  LUXURY CSS — Carbon Black + Amber Gold
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');
 
:root {
    --bg:         #080a0e;
    --bg-card:    #0e1118;
    --bg-glass:   rgba(14, 17, 24, 0.92);
    --gold:       #c8a84b;
    --gold-lt:    #e5c96b;
    --gold-dim:   rgba(200, 168, 75, 0.12);
    --gold-glow:  rgba(200, 168, 75, 0.30);
    --silver:     #a0a8b8;
    --text:       #edeae4;
    --muted:      #5a6070;
    --border:     rgba(200, 168, 75, 0.22);
    --border-hi:  rgba(200, 168, 75, 0.55);
    --red:        #e04040;
    --blue:       #4080e0;
}
 
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Exo 2', sans-serif !important;
}
 
/* Grid background */
.stApp {
    background:
        linear-gradient(rgba(200,168,75,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(200,168,75,0.025) 1px, transparent 1px),
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(200,168,75,0.07), transparent),
        var(--bg) !important;
    background-size: 48px 48px, 48px 48px, auto, auto !important;
}
 
.block-container { padding-top: 0 !important; max-width: 1140px !important; }
#MainMenu, footer, header { visibility: hidden !important; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 2px; }
 
/* ── HERO ── */
.hero {
    text-align: center;
    padding: 2.8rem 0 1.6rem;
    position: relative;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.42em;
    color: var(--gold);
    text-transform: uppercase;
    background: var(--gold-dim);
    border: 1px solid var(--border);
    padding: 5px 18px 4px;
    clip-path: polygon(10px 0%, 100% 0%, calc(100% - 10px) 100%, 0% 100%);
    margin-bottom: 1.1rem;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2.6rem, 5vw, 4.2rem);
    font-weight: 700;
    letter-spacing: 0.08em;
    line-height: 0.95;
    margin: 0 0 0.5rem;
    background: linear-gradient(160deg, #f7e8b0 0%, #c8a84b 40%, #7a5a18 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.78rem;
    letter-spacing: 0.22em;
    color: var(--muted);
    font-weight: 300;
    font-style: italic;
}
.hero-rule {
    width: 100px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.3rem auto 0;
}
 
/* ── CARDS ── */
.g-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.g-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--gold) 40%, var(--gold-lt) 60%, transparent 100%);
}
.g-card::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 80px; height: 80px;
    background: radial-gradient(circle, var(--gold-dim), transparent 70%);
    pointer-events: none;
}
 
.g-card-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.38em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.g-card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}
 
/* ── RESULT PANEL ── */
.result-panel {
    background: linear-gradient(135deg, rgba(200,168,75,0.10), rgba(200,168,75,0.03));
    border: 1px solid var(--gold);
    border-radius: 3px;
    padding: 2rem 2.2rem 1.8rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.result-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-lt), transparent);
}
.result-panel::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(200,168,75,0.12), transparent 65%);
    pointer-events: none;
}
.rp-tag {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.4em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.rp-price {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3.4rem;
    font-weight: 700;
    color: var(--gold-lt);
    line-height: 1;
    letter-spacing: 0.03em;
}
.rp-range {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.5rem;
    letter-spacing: 0.08em;
}
.rp-range b { color: var(--gold); font-weight: 600; }
 
/* ── STAT CHIPS ── */
.stat-row {
    display: flex;
    gap: 10px;
    margin: 1rem 0;
}
.stat-chip {
    flex: 1;
    background: rgba(10, 12, 18, 0.8);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 10px 8px;
    text-align: center;
}
.stat-chip .sc-label {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    color: var(--muted);
    text-transform: uppercase;
    display: block;
    margin-bottom: 3px;
}
.stat-chip .sc-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
}
 
/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 1.2rem 0 0.5rem;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}
 
/* ── PLACEHOLDER ── */
.placeholder {
    text-align: center;
    padding: 5rem 2rem;
    color: var(--muted);
}
.placeholder .ico {
    font-size: 3.5rem;
    opacity: 0.3;
    display: block;
    margin-bottom: 1rem;
}
.placeholder p {
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    line-height: 1.7;
}
.placeholder b { color: var(--gold); }
 
/* ── COMPARE RESULT ── */
.vs-price-card {
    border-radius: 3px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.vpc-a { background: rgba(64,128,224,0.08); border: 1px solid rgba(64,128,224,0.4); }
.vpc-b { background: rgba(224,128,40,0.08); border: 1px solid rgba(224,128,80,0.4); }
.vpc-tag { font-size: 0.6rem; letter-spacing: 0.3em; font-weight: 700; margin-bottom: 4px; text-transform: uppercase; }
.vpc-a .vpc-tag { color: #6ea8f8; }
.vpc-b .vpc-tag { color: #f8a06e; }
.vpc-price {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
}
.vpc-a .vpc-price { color: #8ec8ff; }
.vpc-b .vpc-price { color: #ffc88e; }
.vpc-sub { font-size: 0.72rem; color: var(--muted); margin-top: 5px; }
 
.vs-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
 
.winner-strip {
    background: var(--gold-dim);
    border: 1px solid var(--border-hi);
    border-radius: 3px;
    padding: 0.9rem 1.5rem;
    text-align: center;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: var(--gold-lt);
    text-transform: uppercase;
    margin: 0.8rem 0 1.2rem;
}
 
/* ── INPUTS OVERRIDE ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    font-family: 'Exo 2', sans-serif !important;
}
 
div[data-baseweb="select"] > div {
    background: rgba(8,10,14,0.95) !important;
    border-color: var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--gold) !important; }
 
input[type="number"] {
    background: rgba(8,10,14,0.95) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 3px !important;
}
 
/* ── BUTTON ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c8a84b 0%, #7a5a18 100%) !important;
    color: #05060a !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.32em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 0 !important;
    width: 100% !important;
    clip-path: polygon(12px 0%, 100% 0%, calc(100% - 12px) 100%, 0% 100%) !important;
    transition: all 0.18s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px var(--gold-glow) !important;
    filter: brightness(1.1) !important;
}
div[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }
 
/* ── TABS ── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 2px !important;
    margin-bottom: 1.2rem !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    padding: 0.7rem 1.6rem !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px !important;
    transition: all 0.15s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
    background: var(--gold-dim) !important;
}
 
/* ── DATAFRAME ── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
}
 
/* ── FOOTER ── */
.luxury-footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--muted);
    text-transform: uppercase;
    font-family: 'Rajdhani', sans-serif;
}
.luxury-footer span { color: var(--border); }
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
 
@st.cache_data
def load_year_ranges():
    """Build a dict of (brand, model) -> (launch_year, current_year) from the dataset."""
    try:
        df = pd.read_csv("car data.csv")
        # normalise column names — handle both 'year'/'Year' and 'name'/'car_name' etc.
        df.columns = df.columns.str.lower().str.strip()
        year_col = next((c for c in df.columns if "year" in c), None)
        name_col = next((c for c in df.columns if c in ("name", "car_name", "car name")), None)
        brand_col = next((c for c in df.columns if c == "brand"), None)
        model_col = next((c for c in df.columns if c == "model"), None)
 
        if year_col is None:
            return {}
 
        ranges = {}
        if brand_col and model_col:
            for (brand, model), grp in df.groupby([brand_col, model_col]):
                yr_min = int(grp[year_col].min())
                ranges[(str(brand).strip(), str(model).strip())] = (yr_min, 2026)
        elif name_col:
            df["_brand"] = df[name_col].str.split().str[0].str.strip()
            df["_model"] = df[name_col].str.split().str[1:].str.join(" ").str.strip()
            for (brand, model), grp in df.groupby(["_brand", "_model"]):
                yr_min = int(grp[year_col].min())
                ranges[(str(brand).strip(), str(model).strip())] = (yr_min, 2026)
        return ranges
    except Exception:
        return {}
 
model, brand_model_map, meta = load_artifacts()
year_ranges = load_year_ranges()
 
fuels         = meta["fuel_types"]
transmissions = meta["transmission_types"]
seller_types  = meta["seller_types"]
owners        = meta["owner_types"]
year_min      = meta["year_min"]
year_max      = meta["year_max"]
km_max        = meta["km_max"]
brands        = sorted(brand_model_map.keys())
 
def get_year_range(brand, model):
    """Return (launch_year, 2026) for this brand+model, falling back to global range."""
    key = (brand.strip(), model.strip())
    if key in year_ranges:
        return year_ranges[key][0], 2026
    # fallback: use brand-level min
    brand_keys = [k for k in year_ranges if k[0] == brand.strip()]
    if brand_keys:
        launch = min(year_ranges[k][0] for k in brand_keys)
        return launch, 2026
    return year_min, 2026
 
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
        row    = build_input(brand, mdl, yr, km_est, fuel, transmission, seller_type, owner)
        years.append(yr)
        prices.append(predict_price(row))
    return years, prices
 
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#5a6070", family="Exo 2, sans-serif", size=11),
    margin=dict(l=0, r=0, t=14, b=0),
    height=230,
)
 
# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">◈ &nbsp;AI Valuation Engine&nbsp; ◈</div>
  <div class="hero-title">AUTOPRICEPRO</div>
  <div class="hero-sub">Precision Used Car Valuation &nbsp;·&nbsp; XGBoost ML &nbsp;·&nbsp; R² 95.46%</div>
  <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["◈  SINGLE VALUATION", "⬡  COMPARE TWO CARS"])
 
# ═══════════════════════════════════════════════
#  TAB 1 — SINGLE VALUATION
# ═══════════════════════════════════════════════
with tab1:
    col_form, col_result = st.columns([1, 1.25], gap="large")
 
    with col_form:
        st.markdown('<div class="g-card"><div class="g-card-title">Vehicle Specification</div>', unsafe_allow_html=True)
 
        sel_brand   = st.selectbox("Brand", brands, key="s_brand")
        models_list = brand_model_map.get(sel_brand, [])
        sel_model   = st.selectbox("Model", models_list, key="s_model")
 
        mdl_yr_min, mdl_yr_max = get_year_range(sel_brand, sel_model)
        mdl_default = min(max(mdl_yr_max - 3, mdl_yr_min), mdl_yr_max)
        st.markdown(
            f'<div style="font-size:0.58rem;letter-spacing:0.22em;color:#c8a84b;'
            f'margin:6px 0 2px;font-family:Rajdhani,sans-serif;font-weight:700;">'
            f'MODEL TIMELINE &nbsp;·&nbsp; {mdl_yr_min} — {mdl_yr_max}</div>',
            unsafe_allow_html=True,
        )
 
        c1, c2 = st.columns(2)
        with c1:
            sel_year = st.slider(
                "Purchase Year",
                min_value=mdl_yr_min,
                max_value=mdl_yr_max,
                value=mdl_default,
                key="s_year",
            )
        with c2:
            sel_km = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key="s_km")
 
        c3, c4 = st.columns(2)
        with c3:
            sel_fuel  = st.selectbox("Fuel Type", fuels, key="s_fuel")
        with c4:
            sel_trans = st.selectbox("Transmission", transmissions, key="s_trans")
 
        c5, c6 = st.columns(2)
        with c5:
            sel_seller = st.selectbox("Seller Type", seller_types, key="s_seller")
        with c6:
            sel_owner = st.selectbox("Owner", owners, key="s_owner")
 
        st.markdown("</div>", unsafe_allow_html=True)
        predict_btn = st.button("PREDICT MARKET VALUE", key="s_btn")
 
    with col_result:
        if predict_btn:
            row   = build_input(sel_brand, sel_model, sel_year, sel_km,
                                sel_fuel, sel_trans, sel_seller, sel_owner)
            price = predict_price(row)
            low, high = price * 0.92, price * 1.08
            age = 2026 - sel_year
 
            st.markdown(f"""
            <div class="result-panel">
              <div class="rp-tag">Estimated Market Value</div>
              <div class="rp-price">{fmt_inr(price)}</div>
              <div class="rp-range">Confidence Range &nbsp;·&nbsp; <b>{fmt_inr(low)}</b> — <b>{fmt_inr(high)}</b></div>
            </div>
            <div class="stat-row">
              <div class="stat-chip"><span class="sc-label">Age</span><span class="sc-val">{age} yrs</span></div>
              <div class="stat-chip"><span class="sc-label">KM Driven</span><span class="sc-val">{sel_km:,}</span></div>
              <div class="stat-chip"><span class="sc-label">Fuel</span><span class="sc-val">{sel_fuel}</span></div>
              <div class="stat-chip"><span class="sc-label">Trans.</span><span class="sc-val">{sel_trans[:4]}</span></div>
            </div>
            """, unsafe_allow_html=True)
 
            # Chart 1: Depreciation Curve
            st.markdown('<div class="sec-label">Depreciation Curve</div>', unsafe_allow_html=True)
            yrs, prices = depreciation_series(
                sel_brand, sel_model, max(sel_year, 2010),
                sel_km, sel_fuel, sel_trans, sel_seller, sel_owner
            )
            fig_dep = go.Figure()
            fig_dep.add_trace(go.Scatter(
                x=yrs, y=[p/1e5 for p in prices],
                mode="lines+markers",
                line=dict(color="#c8a84b", width=2.5),
                marker=dict(size=5, color="#e5c96b", line=dict(color="#c8a84b", width=1)),
                fill="tozeroy",
                fillcolor="rgba(200,168,75,0.06)",
                name="Value (₹ Lakh)",
            ))
            fig_dep.update_layout(
                **PLOT_LAYOUT,
                xaxis=dict(title="Year", gridcolor="rgba(200,168,75,0.07)", showgrid=True, zeroline=False),
                yaxis=dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", showgrid=True, zeroline=False),
            )
            st.plotly_chart(fig_dep, use_container_width=True)
 
            # Chart 2: Price vs KM
            st.markdown('<div class="sec-label">Price vs KM Driven</div>', unsafe_allow_html=True)
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
                line=dict(color="#a0a8b8", width=2),
                fill="tozeroy",
                fillcolor="rgba(160,168,184,0.05)",
            ))
            fig_km.add_vline(
                x=sel_km,
                line_dash="dot", line_color="#c8a84b", line_width=1.5,
                annotation_text=f"  {sel_km:,} km",
                annotation_font_color="#c8a84b",
                annotation_font_size=10,
            )
            fig_km.update_layout(
                **PLOT_LAYOUT,
                xaxis=dict(title="KM Driven", gridcolor="rgba(200,168,75,0.07)", tickformat=",", zeroline=False),
                yaxis=dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", zeroline=False),
            )
            st.plotly_chart(fig_km, use_container_width=True)
 
        else:
            st.markdown("""
            <div class="placeholder">
              <span class="ico">◈</span>
              <p>Configure vehicle specifications<br>and press<br>
              <b>PREDICT MARKET VALUE</b></p>
            </div>
            """, unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════
#  TAB 2 — COMPARISON MODE
# ═══════════════════════════════════════════════
with tab2:
    cc1, cc2 = st.columns(2, gap="large")
 
    def car_form(col, idx):
        color_label = "CAR A — BLUE" if idx == 1 else "CAR B — AMBER"
        with col:
            st.markdown(f'<div class="g-card"><div class="g-card-title">{color_label}</div>', unsafe_allow_html=True)
            brand    = st.selectbox("Brand", brands, key=f"c{idx}_brand")
            mdl_list = brand_model_map.get(brand, [])
            mdl      = st.selectbox("Model", mdl_list, key=f"c{idx}_model")
            c_yr_min, c_yr_max = get_year_range(brand, mdl)
            c_default = min(max(c_yr_max - 3, c_yr_min), c_yr_max)
            st.markdown(
                f"<div style='font-size:0.58rem;letter-spacing:0.22em;color:#c8a84b;"
                f"margin:6px 0 2px;font-family:Rajdhani,sans-serif;font-weight:700;'>"
                f"TIMELINE &nbsp;·&nbsp; {c_yr_min} — {c_yr_max}</div>",
                unsafe_allow_html=True,
            )
            yr       = st.slider("Purchase Year", min_value=c_yr_min, max_value=c_yr_max, value=c_default, key=f"c{idx}_year")
            km       = st.number_input("KM Driven", min_value=0, max_value=km_max, value=13000, step=1, key=f"c{idx}_km")
            fuel     = st.selectbox("Fuel Type", fuels, key=f"c{idx}_fuel")
            trans    = st.selectbox("Transmission", transmissions, key=f"c{idx}_trans")
            seller   = st.selectbox("Seller Type", seller_types, key=f"c{idx}_seller")
            owner    = st.selectbox("Owner", owners, key=f"c{idx}_owner")
            st.markdown("</div>", unsafe_allow_html=True)
        return brand, mdl, yr, km, fuel, trans, seller, owner
 
    data_a = car_form(cc1, 1)
    data_b = car_form(cc2, 2)
 
    compare_btn = st.button("RUN COMPARISON ANALYSIS", key="cmp_btn")
 
    if compare_btn:
        brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a = data_a
        brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b = data_b
 
        row_a   = build_input(brand_a, mdl_a, yr_a, km_a, fuel_a, trans_a, seller_a, owner_a)
        row_b   = build_input(brand_b, mdl_b, yr_b, km_b, fuel_b, trans_b, seller_b, owner_b)
        price_a = predict_price(row_a)
        price_b = predict_price(row_b)
        winner  = f"CAR A  ({brand_a} {mdl_a})" if price_a >= price_b else f"CAR B  ({brand_b} {mdl_b})"
        diff    = abs(price_a - price_b)
 
        r1, r2, r3 = st.columns([1, 0.18, 1])
        with r1:
            st.markdown(f"""
            <div class="vs-price-card vpc-a">
              <div class="vpc-tag">Car A · {brand_a} {mdl_a}</div>
              <div class="vpc-price">{fmt_inr(price_a)}</div>
              <div class="vpc-sub">{yr_a} &nbsp;·&nbsp; {km_a:,} km &nbsp;·&nbsp; {fuel_a}</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="vs-divider" style="height:100%;padding-top:1rem;">VS</div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="vs-price-card vpc-b">
              <div class="vpc-tag">Car B · {brand_b} {mdl_b}</div>
              <div class="vpc-price">{fmt_inr(price_b)}</div>
              <div class="vpc-sub">{yr_b} &nbsp;·&nbsp; {km_b:,} km &nbsp;·&nbsp; {fuel_b}</div>
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown(f"""
        <div class="winner-strip">
            ◈ &nbsp; Higher Value: &nbsp; {winner} &nbsp; · &nbsp; Difference: {fmt_inr(diff)} &nbsp; ◈
        </div>
        """, unsafe_allow_html=True)
 
        ch1, ch2 = st.columns(2)
 
        with ch1:
            st.markdown('<div class="sec-label">Price Comparison</div>', unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                x=[f"{brand_a} {mdl_a}", f"{brand_b} {mdl_b}"],
                y=[price_a / 1e5, price_b / 1e5],
                marker_color=["#4080e0", "#e08040"],
                marker_line_color=["#6ea8f8", "#f8a06e"],
                marker_line_width=1,
                text=[fmt_inr(price_a), fmt_inr(price_b)],
                textposition="outside",
                textfont=dict(color="#c8a84b", size=12, family="Rajdhani"),
            ))
            fig_bar.update_layout(
                **PLOT_LAYOUT,
                height=280,
                yaxis=dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", zeroline=False),
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
 
        with ch2:
            st.markdown('<div class="sec-label">Depreciation Comparison</div>', unsafe_allow_html=True)
            yrs_a, dep_a = depreciation_series(brand_a, mdl_a, max(yr_a, 2010), km_a, fuel_a, trans_a, seller_a, owner_a)
            yrs_b, dep_b = depreciation_series(brand_b, mdl_b, max(yr_b, 2010), km_b, fuel_b, trans_b, seller_b, owner_b)
 
            fig_dep2 = go.Figure()
            fig_dep2.add_trace(go.Scatter(
                x=yrs_a, y=[p/1e5 for p in dep_a],
                name=f"{brand_a} {mdl_a}",
                line=dict(color="#4080e0", width=2.5),
                mode="lines+markers",
                marker=dict(size=4),
            ))
            fig_dep2.add_trace(go.Scatter(
                x=yrs_b, y=[p/1e5 for p in dep_b],
                name=f"{brand_b} {mdl_b}",
                line=dict(color="#e08040", width=2.5),
                mode="lines+markers",
                marker=dict(size=4),
            ))
            fig_dep2.update_layout(
                **PLOT_LAYOUT,
                height=280,
                xaxis=dict(title="Year", gridcolor="rgba(200,168,75,0.07)", zeroline=False),
                yaxis=dict(title="₹ Lakh", gridcolor="rgba(200,168,75,0.07)", zeroline=False),
                legend=dict(
                    bgcolor="rgba(8,10,14,0.8)",
                    bordercolor="rgba(200,168,75,0.2)",
                    borderwidth=1,
                    font=dict(color="#a0a8b8", size=10),
                ),
            )
            st.plotly_chart(fig_dep2, use_container_width=True)
 
        # Spec Table
        st.markdown('<div class="sec-label">Specifications</div>', unsafe_allow_html=True)
        specs_df = pd.DataFrame({
            "Specification":     ["Brand", "Model", "Year", "KM Driven", "Fuel", "Transmission", "Seller", "Owner", "Est. Price"],
            f"Car A  {brand_a}": [brand_a, mdl_a, yr_a, f"{km_a:,} km", fuel_a, trans_a, seller_a, owner_a, fmt_inr(price_a)],
            f"Car B  {brand_b}": [brand_b, mdl_b, yr_b, f"{km_b:,} km", fuel_b, trans_b, seller_b, owner_b, fmt_inr(price_b)],
        })
        st.dataframe(specs_df.set_index("Specification"), use_container_width=True)
 
## ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="luxury-footer">
    AutoPricePro &nbsp;·&nbsp; XGBoost ML Engine &nbsp;·&nbsp; R² 95.46%
    &nbsp;<span>|</span>&nbsp;
    Predictions are estimates — verify before transacting
</div>
""", unsafe_allow_html=True)
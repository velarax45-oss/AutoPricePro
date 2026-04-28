# ============================================================
# AutoPricePro — Model Training Script
# Run this once to generate AutoPricePro.pkl + brand_model_map.pkl
# ============================================================

# 📌 CELL 1 — Imports
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

# ============================================================
# 📌 CELL 2 — Load Dataset
# ============================================================
df = pd.read_csv("Car details v3.csv")
print("✅ Dataset loaded:", df.shape)
print(df.head())
print(df.columns.tolist())

# ============================================================
# 📌 CELL 3 — Keep only clean columns
# ============================================================
df = df[[
    "name",
    "year",
    "km_driven",
    "fuel",
    "seller_type",
    "transmission",
    "owner",
    "selling_price"
]].copy()

# Drop rows with any nulls in these columns
df.dropna(inplace=True)
print(f"✅ After column filter & dropna: {df.shape}")

# ============================================================
# 📌 CELL 4 — Feature Engineering (FIXED)
# ============================================================
df["brand"] = df["name"].str.split().str[0]

# Row-wise replace so brand is always a scalar string
df["model"] = df.apply(
    lambda row: row["name"].replace(row["brand"] + " ", "", 1)
    if pd.notna(row["name"]) and pd.notna(row["brand"])
    else np.nan,
    axis=1
)

df["age"] = 2026 - df["year"]
df["km_log"] = np.log1p(df["km_driven"])

# Clean up
df.dropna(subset=["brand", "model"], inplace=True)
df = df[df["model"].str.strip() != ""]
df = df[df["brand"].str.strip() != ""]

print(f"✅ After feature engineering: {df.shape}")
print(f"   Unique brands : {df['brand'].nunique()}")
print(f"   Unique models : {df['model'].nunique()}")

# ============================================================
# 📌 CELL 5 — Define Features & Target
# ============================================================
FEATURES = ["brand", "model", "age", "km_log", "fuel",
            "seller_type", "transmission", "owner"]

X = df[FEATURES]
y = df["selling_price"]

# ============================================================
# 📌 CELL 6 — Train / Test Split
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Train: {X_train.shape}  |  Test: {X_test.shape}")

# ============================================================
# 📌 CELL 7 — Preprocessing
# ============================================================
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = [c for c in FEATURES if c not in cat_cols]

print(f"   Categorical : {cat_cols}")
print(f"   Numerical   : {num_cols}")

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
    ],
    remainder="passthrough"
)

# ============================================================
# 📌 CELL 8 — Model Pipeline
# ============================================================
AutoPricePro = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", XGBRegressor(
        n_estimators=700,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        tree_method="hist",       # faster training
        device="cpu"
    ))
])

# ============================================================
# 📌 CELL 9 — Train
# ============================================================
print("⏳ Training model...")
AutoPricePro.fit(X_train, y_train)
print("✅ Training complete!")

# ============================================================
# 📌 CELL 10 — Evaluate
# ============================================================
pred = AutoPricePro.predict(X_test)
r2  = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)

print("=" * 40)
print(f"  R²  Score : {r2:.4f}")
print(f"  MAE       : ₹{mae:,.0f}")
print("=" * 40)

# ============================================================
# 📌 CELL 11 — Save Model + Brand→Model Lookup
# ============================================================
joblib.dump(AutoPricePro, "AutoPricePro.pkl")
print("✅ Saved: AutoPricePro.pkl")

# Build clean brand → sorted model list mapping
brand_model_map = (
    df.groupby("brand")["model"]
    .apply(lambda x: sorted(x.dropna().unique().tolist()))
    .to_dict()
)
joblib.dump(brand_model_map, "brand_model_map.pkl")
print(f"✅ Saved: brand_model_map.pkl  ({len(brand_model_map)} brands)")

# Save metadata for the app
meta = {
    "fuel_types"       : sorted(df["fuel"].unique().tolist()),
    "transmission_types": sorted(df["transmission"].unique().tolist()),
    "seller_types"     : sorted(df["seller_type"].unique().tolist()),
    "owner_types"      : df["owner"].unique().tolist(),
    "year_min"         : int(df["year"].min()),
    "year_max"         : int(df["year"].max()),
    "km_min"           : int(df["km_driven"].min()),
    "km_max"           : int(df["km_driven"].max()),
}
joblib.dump(meta, "meta.pkl")
print("✅ Saved: meta.pkl")
print("\n🎉 All done! Run:  streamlit run app.py")

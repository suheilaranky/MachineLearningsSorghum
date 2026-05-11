import numpy as np
import pandas as pd
import joblib
import sklearn

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Training with scikit-learn:", sklearn.__version__)

# Load dataset
df = pd.read_csv("wfp_food_prices_sdn.csv")

# Prepare date
df["date"] = pd.to_datetime(df["date"])
df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.month

# Select Sorghum data
df_crop = df[
    (df["commodity"] == "Sorghum") &
    (df["unit"] == "3 KG") &
    (df["pricetype"] == "Retail")
].copy()

# Exclude 2025 and later if you want
df_crop = df_crop[df_crop["Year"] <= 2024].copy()

# Select columns
df_model = df_crop[["Year", "Month", "admin1", "market", "usdprice"]].copy()
df_model = df_model.rename(columns={"usdprice": "Price_USD"})
df_model = df_model.dropna()

# Optional: remove extreme outliers
upper_limit = df_model["Price_USD"].quantile(0.99)
df_model = df_model[df_model["Price_USD"] <= upper_limit].copy()

X = df_model[["Year", "Month", "admin1", "market"]]
y = df_model["Price_USD"]

categorical_features = ["admin1", "market"]
numeric_features = ["Year", "Month"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

rf_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(random_state=42))
])

param_grid = {
    "model__n_estimators": [50, 100],
    "model__max_depth": [10, 20, None],
    "model__min_samples_split": [2, 5],
    "model__min_samples_leaf": [1, 2]
}

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

grid_rf = GridSearchCV(
    estimator=rf_model,
    param_grid=param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

grid_rf.fit(X_train, y_train)

best_model = grid_rf.best_estimator_

y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Best parameters:", grid_rf.best_params_)
print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)

joblib.dump(best_model, "optimized_sorghum_price_model.pkl")

print("Saved model: optimized_sorghum_price_model.pkl")
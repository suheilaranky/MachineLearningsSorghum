import streamlit as st
import pandas as pd
import joblib
import sklearn

st.write("scikit-learn version:", sklearn.__version__)

model = joblib.load("optimized_sorghum_price_model.pkl")

st.title("Sorghum Price Prediction in Sudan")

year = st.selectbox("Select Year", list(range(2024, 2031)))
month = st.selectbox("Select Month", list(range(1, 13)))

admin1 = st.selectbox("Select State", [
    "Khartoum", "Al Jazirah", "Blue Nile", "Central Darfur",
    "East Darfur", "Gedaref", "Kassala", "North Darfur",
    "North Kordofan", "Northern", "Red Sea", "River Nile",
    "Sennar", "South Darfur", "South Kordofan", "West Darfur",
    "West Kordofan", "White Nile"
])

market = st.selectbox("Select Market", [
    "Khartoum", "Wad Medani", "Damazin", "Zalingei",
    "Ed Daein", "Gedaref", "Kassala", "El Fasher",
    "El Obeid", "Dongola", "Port Sudan", "Atbara",
    "Sennar", "Nyala", "Kadugli", "El Geneina",
    "El Fula", "Kosti"
])
exchange_rate = st.number_input(
    "Enter exchange rate: 1 USD = how many SDG?",
    min_value=0.0,
    value=600.0,
    step=10.0
)


if st.button("Predict Price"):
    new_data = pd.DataFrame({
        "Year": [year],
        "Month": [month],
        "admin1": [admin1],
        "market": [market]
    })

    prediction_3kg_usd = model.predict(new_data)[0]

    # One shwal = 28 units of 3 KG
    prediction_shwal_usd = prediction_3kg_usd * 28

    # Convert to SDG
    prediction_3kg_sdg = prediction_3kg_usd * exchange_rate
    prediction_shwal_sdg = prediction_shwal_usd * exchange_rate

    st.success(f"Predicted Price for 3 KG: {prediction_3kg_usd:.2f} USD")
    st.success(f"Predicted Price for 3 KG: {prediction_3kg_sdg:,.2f} SDG")

    st.success(f"Predicted Price for 1 Shwal (84 KG): {prediction_shwal_usd:.2f} USD")
    st.success(f"Predicted Price for 1 Shwal (84 KG): {prediction_shwal_sdg:,.2f} SDG")

    st.info("One shwal is calculated as 28 units of 3 KG = 84 KG.")
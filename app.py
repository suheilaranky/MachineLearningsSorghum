import streamlit as st
import pandas as pd
import joblib
import os

# ===============================
# إعدادات الصفحة
# ===============================
st.set_page_config(
    page_title="التنبؤ بسعر الذرة الرفيعة",
    page_icon="🌾",
    layout="centered"
)

# ===============================
# جعل الواجهة من اليمين إلى اليسار RTL
# ===============================
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
    }

    .stApp {
        direction: rtl;
        text-align: right;
    }

    div[data-testid="stMarkdownContainer"] {
        direction: rtl;
        text-align: right;
    }

    label {
        direction: rtl;
        text-align: right;
    }

    .stSelectbox label {
        direction: rtl;
        text-align: right;
    }

    .stNumberInput label {
        direction: rtl;
        text-align: right;
    }

    .stButton button {
        direction: rtl;
        text-align: center;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌾 التنبؤ بسعر الذرة الرفيعة في السودان")
st.write("واجهة بسيطة تستخدم نموذج تعلم آلة للتنبؤ بسعر الذرة الرفيعة بالدولار الأمريكي، مع تحويله تقريبيًا إلى الجنيه السوداني.")

# ===============================
# تحميل النموذج
# ===============================
model_path = "optimized_sorghum_price_model.pkl"

if not os.path.exists(model_path):
    st.error("ملف النموذج غير موجود. تأكدي أن ملف optimized_sorghum_price_model.pkl موجود في نفس مجلد app.py")
    st.stop()

try:
    model = joblib.load(model_path)
    st.success("تم تحميل النموذج بنجاح ✅")
except Exception as e:
    st.error("حدث خطأ أثناء تحميل النموذج ❌")
    st.write("تفاصيل الخطأ:")
    st.code(str(e))
    st.stop()

st.markdown("---")

# ===============================
# ربط الولاية بالسوق
# ===============================
wilaya_market = {
    "Khartoum": "Khartoum",
    "Al Jazirah": "Wad Medani",
    "Blue Nile": "Damazin",
    "Central Darfur": "Zalingei",
    "East Darfur": "Ed Daein",
    "Gedaref": "Gedaref",
    "Kassala": "Kassala",
    "North Darfur": "El Fasher",
    "North Kordofan": "El Obeid",
    "Northern": "Dongola",
    "Red Sea": "Port Sudan",
    "River Nile": "Atbara",
    "Sennar": "Sennar",
    "South Darfur": "Nyala",
    "South Kordofan": "Kadugli",
    "West Darfur": "El Geneina",
    "West Kordofan": "El Fula",
    "White Nile": "Kosti"
}

# ===============================
# إدخالات المستخدم
# ===============================
year = st.selectbox(
    "اختر السنة",
    list(range(2024, 2031))
)

month = st.selectbox(
    "اختر الشهر",
    list(range(1, 13))
)

admin1 = st.selectbox(
    "اختر الولاية",
    list(wilaya_market.keys())
)

market = wilaya_market[admin1]

st.info(f"السوق المرتبط بهذه الولاية هو: {market}")

exchange_rate = st.number_input(
    "أدخل سعر صرف الدولار مقابل الجنيه السوداني",
    min_value=1.0,
    value=2500.0,
    step=50.0
)

st.markdown("---")

# ===============================
# التنبؤ
# ===============================
if st.button("توقع السعر"):
    new_data = pd.DataFrame({
        "Year": [year],
        "Month": [month],
        "admin1": [admin1],
        "market": [market]
    })

    # ===============================
# التنبؤ
# ===============================


    try:
        # السعر المتوقع لـ 3 كيلو بالدولار
        prediction_usd_3kg = model.predict(new_data)[0]

        # تحويل السعر إلى جنيه سوداني لـ 3 كيلو
        prediction_sdg_3kg = prediction_usd_3kg * exchange_rate

        # حساب سعر الجوال 90 كيلو
        prediction_usd_90kg = prediction_usd_3kg * 30
        prediction_sdg_90kg = prediction_sdg_3kg * 30

  
        st.markdown("---")

        st.success(f"سعر جوال الذرة المتوقع   هو: {prediction_usd_90kg:.2f} دولار أمريكي")
        st.success(f"سعر جوال الذرة المتوقع   بالجنيه السوداني هو: {prediction_sdg_90kg:,.2f} جنيه سوداني")

    
    except Exception as e:
        st.error("حدث خطأ أثناء التنبؤ بالسعر ❌")
        st.write("تفاصيل الخطأ:")
        st.code(str(e))
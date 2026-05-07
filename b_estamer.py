
# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.3 CEMENT & STEEL EMPIRE - All Rights Reserved
# Unauthorized copying, modification, distribution prohibited
# Contact: uwayobruno3@gmail.com | +250787993679

import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import re

st.set_page_config(page_title="B-ESTAMER V3.3 EMPIRE", layout="wide")
st.title("B-ESTAMER V3.3 CEMENT & STEEL EMPIRE 👑")

# --- 1. PDF/IMAGE UPLOAD SECTION ---
st.header("1. UPLOAD PLAN")
uploaded_file = st.file_uploader("Upload Plan PDF/Image", type=["pdf","png","jpg","jpeg"])

auto_dimensions = {"length": 0, "width": 0, "height": 0}

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            st.success(f"PDF yasomwe. Pages: {len(pdf.pages)}")
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() or ""
            numbers = re.findall(r'(\d+[.,]?\d*)\s*(m|mm|cm)', all_text.lower())
            if numbers:
                st.info(f"Numbers zabonetse: {numbers[:5]}")
                if len(numbers) >= 1: auto_dimensions["length"] = float(numbers[0][0].replace(',','.'))
                if len(numbers) >= 2: auto_dimensions["width"] = float(numbers[1][0].replace(',','.'))
                if len(numbers) >= 3: auto_dimensions["height"] = float(numbers[2][0].replace(',','.'))
    else:
        st.image(Image.open(uploaded_file), caption="Uploaded Plan", use_column_width=True)
        st.warning("Auto-extract kuri image iri coming soon. Shyiramo dimensions hasi.")

# --- 2. MATERIALS & RATES SECTION ---
st.header("2. MATERIALS & RATES")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Cement Types RWF/50kg")
    cement_325 = st.number_input("CEM II 32.5R", value=12500, key="cem325")
    cement_425 = st.number_input("CEM II 42.5N", value=13500, key="cem425")
    cement_525 = st.number_input("CEM I 52.5N", value=15000, key="cem525")
    cement_type = st.selectbox("Select Cement Grade", ["CEM II 32.5R", "CEM II 42.5N", "CEM I 52.5N"])

with col2:
    st.subheader("Steel Prices RWF/kg")
    r6 = st.number_input("R6 Price", value=1200, key="r6")
    r8 = st.number_input("R8 Price", value=1200, key="r8")
    r10 = st.number_input("R10 Price", value=1200, key="r10")
    r12 = st.number_input("R12 Price", value=1200, key="r12")
    y16 = st.number_input("Y16 Price", value=1250, key="y16")
    y20 = st.number_input("Y20 Price", value=1250, key="y20")
    y25 = st.number_input("Y25 Price", value=1300, key="y25")
    y40 = st.number_input("Y40 Price", value=1400, key="y40")

with col3:
    st.subheader("Concrete Mix Ratios")
    c15 = st.text_input("C15 (1:3:6)", value="1:3:6", key="c15")
    c20 = st.text_input("C20 (1:2:4)", value="1:2:4", key="c20")
    c25 = st.text_input("C25 (1:1.5:3)", value="1:1.5:3", key="c25")
    c30 = st.text_input("C30 (1:1:2)", value="1:1:2", key="c30")
    c35 = st.text_input("C35 (1:1:1)", value="1:1:1", key="c35")
    concrete_grade = st.selectbox("Select Concrete Grade", ["C15", "C20", "C25", "C30", "C35"])

# --- 3. AUTO BOQ GENERATION ---
st.header("3. AUTO BOQ")
st.info("Shyiramo dimensions. Niba warakoze upload, zakwiyuzamo automatic.")

col_a, col_b, col_c = st.columns(3)
with col_a:
    length = st.number_input("Length (m)", value=auto_dimensions["length"], key="len")
with col_b:
    width = st.number_input("Width (m)", value=auto_dimensions["width"], key="wid")
with col_c:
    height = st.number_input("Height (m)", value=auto_dimensions["height"], key="hei")

area = length * width
volume = length * width * height

items = [
    ["A", "SUBSTRUCTURE", "", "", "", ""],
    [1, "Site Clearance", area, "m²", 500, area * 500],
    [2, f"Excavation for foundation", volume, "m³", 3500, volume * 3500],
    [3, f"Concrete {concrete_grade} in foundation", volume * 0.4, "m³", 180000, volume * 0.4 * 180000],
    [4, "Y16 Steel in foundation", volume * 80, "kg", y16, volume * 80 * y16],
    ["B", "SUPERSTRUCTURE", "", "", "", ""],
    [5, f"Concrete {concrete_grade} in columns", height * 0.2, "m³", 200000, height * 0.2 * 200000],
    [6, "Y40 Steel in columns", height * 100, "kg", y40, height * 100 * y40],
    [7, f"Cement {cement_type} for mortar", area * 0.5, "bags", cement_525 if cement_type == "CEM I 52.5N" else cement_425 if cement_type == "CEM II 42.5N" else cement_325, area * 0.5 * (cement_525 if cement_type == "CEM I 52.5N" else cement_425 if cement_type == "CEM II 42.5N" else cement_325)]
]

df = pd.DataFrame(items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])

# Calculate totals
subtotal = df[df["Amount"]!= ""]["Amount"].sum()
vat = subtotal * 0.18
grand_total = subtotal + vat

# Display BOQ
st.dataframe(df, use_container_width=True)

col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("SUB TOTAL", f"{subtotal:,.0f} RWF")
col_t2.metric("VAT 18%", f"{vat:,.0f} RWF")
col_t3.metric("GRAND TOTAL", f"{grand_total:,.0f} RWF")

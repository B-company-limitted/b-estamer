# ================================================================
# COPYRIGHT © 2026 CEO BRUNO - B-ESTAMER PRO RWANDA V3.1
# ALL RIGHTS RESERVED - PATENT PENDING  
# UNAUTHORIZED COPYING, USE, OR DISTRIBUTION = 10,000,000 RWF PENALTY
# COMMERCIAL LICENSE: WhatsApp +250787993679 | Email: uwayobruno32gmail.coml
# RPPA COMPLIANT QS ENGINE - BUILT FOR RWANDA
# ================================================================
import streamlit as st
import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image
import re
from io import BytesIO
# SOMA STEEL MURI SECRETS - ENCRYPTED
prices_json = st.secrets["PRICES_DATA"]
prices_dict = json.loads(prices_json)
prices_df = pd.DataFrame(prices_dict)
st.set_page_config(page_title="B-ESTAMER V3.1 PRO", layout="wide", initial_sidebar_state="expanded")

if 'boq_df' not in st.session_state:
    st.session_state.boq_df = pd.DataFrame()

st.title("🏗️ B-ESTAMER V3.1 PRO - FULL QS ENGINE")
st.caption("Auto Plan Scan OR Manual → Complete RPPA BOQ na Amatafari")

# 1. SIDEBAR: PROJECT + MATERIALS
st.sidebar.header("⚙️ 1. PROJECT SETTINGS")
mode = st.sidebar.radio("Mode:", ["Auto - Soma Plan", "Manual - Andika Measurements"])
profit = st.sidebar.slider("Profit Margin %", 0, 50, 15)

st.sidebar.divider()
st.sidebar.header("🧱 2. MATERIALS & RATES")

# WALL MATERIALS - INCLUDING BRICKS
wall_material = st.sidebar.selectbox("Material y'Inkuta",
    ["Blocks 15cm", "Blocks 20cm", "Blocks 10cm", "Amatafari", "Stone"])

if "Blocks" in wall_material:
    wall_rate = st.sidebar.number_input(f"Rate {wall_material} (RWF/Pc)", 500, 5000, 1000)
    wall_unit = "Pcs"
    blocks_per_m2 = 12 if "15cm" in wall_material else 10 if "20cm" in wall_material else 15
elif "Amatafari" in wall_material:
    wall_rate = st.sidebar.number_input("Rate Amatafari (RWF/Pc)", 100, 1000, 300)
    wall_unit = "Pcs"
    blocks_per_m2 = 50 # 50 bricks per m² wall
else: # Stone
    wall_rate = st.sidebar.number_input("Rate Stone (RWF/m3)", 10000, 50000, 25000)
    wall_unit = "m3"
    blocks_per_m2 = 0.15 # 0.15 m3 stone per m² wall

# Other Materials
cement_type = st.sidebar.selectbox("Cement", ["Cement 32.5", "Cement 42.5"])
cement_rate = st.sidebar.number_input(f"Rate {cement_type} (RWF/Bag)", 10000, 25000, 13000)
steel_type = st.sidebar.selectbox("Steel", ["Steel Y12", "Steel Y10", "Steel Y16"])
steel_rate = st.sidebar.number_input(f"Rate {steel_type} (RWF/Kg)", 1000, 3000, 1800)
sand_rate = st.sidebar.number_input("Sand (RWF/Trip)", 30000, 150000, 70000)
concrete_rate = st.sidebar.number_input("Concrete C20 (RWF/m3)", 100000, 200000, 140000)
roof_type = st.sidebar.selectbox("Roofing", ["Mabati", "Tiles", "Slab"])
roof_rate = st.sidebar.number_input(f"Rate {roof_type} (RWF/m2)", 5000, 30000, 12000)
paint_rate = st.sidebar.number_input("Paint 3 coats (RWF/m2)", 1000, 5000, 2500)

# 2. MAIN INPUT
st.header("📐 3. DIMENSIONS")
col1, col2, col3 = st.columns(3)
length, width, height = 0, 0, 3.0

if mode == "Auto - Soma Plan":
    uploaded_file = st.file_uploader("Upload Plan PDF/Image", type=["pdf", "png", "jpg"])
    if uploaded_file:
        text = ""
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        else:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
        dims = re.findall(r'(\d+\.\d{3})', text)
        if len(dims) >= 2:
            length, width = float(dims[0]), float(dims[1])
            st.success(f"Auto Detected: {length}m x {width}m")
        else:
            st.warning("Sinabona dimensions. Koresha Manual.")
else:
    length = col1.number_input("Length (m)", 1.0, 100.0, 11.401)
    width = col2.number_input("Width (m)", 1.0, 100.0, 8.931)
    height = col3.number_input("Wall Height (m)", 2.0, 5.0, 3.0)

# 3. GENERATE BOQ
if st.button("🚀 GENERATE FULL BOQ", type="primary", use_container_width=True):
    if length > 0 and width > 0:
        area = length * width
        perimeter = (length + width) * 2
        wall_area = perimeter * height

        # QS CALCULATIONS - 25+ ITEMS NA BRICKS
        cement_factor = 0.5 if "42.5" in cement_type else 0.6
        wall_qty = wall_area * blocks_per_m2

        items = [
            ["A", "SUBSTRUCTURE", "", "", "", ""],
            [1, "Site Clearance", area, "m²", 500, area * 500],
            [2, "Excavation foundation", area * 0.5, "m3", 3000, area * 0.5 * 3000],
            [3, "Hardcore 200mm", area * 0.2, "m3", 15000, area * 0.2 * 15000],
            [4, "Concrete blinding C10", area * 0.05, "m3", 120000, area * 0.05 * 120000],
            [5, "Foundation footing C20", area * 0.15, "m3", concrete_rate, area * 0.15 * concrete_rate],
            [6, "DPC Membrane", area, "m²", 2000, area * 2000],
            ["B", "SUPERSTRUCTURE", "", "", "", ""],
            [7, wall_material, wall_qty, wall_unit, wall_rate, wall_qty * wall_rate],
            [8, cement_type + " - Mortar", area * cement_factor, "Bags", cement_rate, area * cement_factor * cement_rate],
            [9, "Sand - Mortar", area * 0.08, "Trips", sand_rate, area * 0.08 * sand_rate],
            [10, steel_type + " - Ring beam", area * 2, "Kg", steel_rate, area * 2 * steel_rate],
            [11, "Ring beam C20", perimeter * 0.12, "m3", concrete_rate, perimeter * 0.12 * concrete_rate],
            [12, "Lintels C20", perimeter * 0.08, "m3", concrete_rate, perimeter * 0.08 * concrete_rate],
            ["C", "ROOFING & FINISHES", "", "", "", ""],
            [13, f"{roof_type} Roofing", area * 1.2, "m²", roof_rate, area * 1.2 * roof_rate],
            [14, "Fascia board", perimeter, "m", 5000, perimeter * 5000],
            [15, "Doors 90x210cm", 4, "Pcs", 80000, 320000],
            [16, "Windows 120x120cm", 6, "Pcs", 60000, 360000],
            [17, "Floor slab C20", area * 0.1, "m3", concrete_rate, area * 0.1 * concrete_rate],
            [18, "Floor tiles", area * 0.8, "m²", 15000, area * 0.8 * 15000],
            [19, "Plastering internal", wall_area * 0.8, "m²", 3000, wall_area * 0.8 * 3000],
            [20, "Plastering external", wall_area * 1.0, "m²", 3500, wall_area * 1.0 * 3500],
            [21, "Paint 3 coats", wall_area * 1.8, "m²", paint_rate, wall_area * 1.8 * paint_rate],
            ["D", "SERVICES", "", "", "", ""],
            [22, "Plumbing - Provisional", 1, "Sum", 500000, 500000],
            [23, "Electrical - Provisional", 1, "Sum", 400000, 400000],
            [24, "Septic tank", 1, "Sum", 300000, 300000],
        ]

        df = pd.DataFrame(items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])
        subtotal = pd.to_numeric(df["Amount"], errors='coerce').sum()
        profit_amt = subtotal * (profit / 100)
        total = subtotal + profit_amt

        df.loc[len(df)] = ["", "SUB-TOTAL", "", "", "", subtotal]
        df.loc[len(df)] = ["", f"Add {profit}% Profit", "", "", "", profit_amt]
        df.loc[len(df)] = ["", "GRAND TOTAL", "", "", "", total]
        st.session_state.boq_df = df
    else:
        st.error("Shyiramo Length na Width byibura.")

# 4. DISPLAY
if not st.session_state.boq_df.empty:
    st.header("📊 4. RPPA BOQ COMPLETE - 25 ITEMS")
    st.dataframe(st.session_state.boq_df, use_container_width=True, hide_index=True)
    total = st.session_state.boq_df["Amount"].iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("AREA", f"{length * width:.1f} m²")
    col2.metric("WALL MATERIAL", wall_material)
    col3.metric("PROFIT", f"{profit}%")
    col4.metric("GRAND TOTAL", f"{total:,.0f} RWF")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.boq_df.to_excel(writer, index=False, sheet_name='BOQ')
    st.download_button("📥 Download Excel RPPA BOQ", output.getvalue(), "BOQ_RPPA_Complete.xlsx", use_container_width=True)

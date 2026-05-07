# ================================================================
# COPYRIGHT © 2026 CEO BRUNO - B-ESTAMER PRO RWANDA V3.1
# ALL RIGHTS RESERVED - PATENT PENDING  
# UNAUTHORIZED COPYING, USE, OR DISTRIBUTION = 10,000,000 RWF PENALTY
# COMMERCIAL LICENSE: WhatsApp +250787993679 | Email: uwayobruno32gmail.coml
# RPPA COMPLIANT QS ENGINE - BUILT FOR RWANDA
# ================================================================
import streamlit as st
import pandas as pd
import json 
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
# ========== 2. MATERIALS & RATES - FULL CEMENT & STEEL EMPIRE ==========
st.header("2. MATERIALS & RATES")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Steel Bars - R6 to Y40")
    steel_prices = {
        "R6": st.number_input("R6 Price RWF/kg", value=1300, key="r6"),
        "R8": st.number_input("R8 Price RWF/kg", value=1250, key="r8"),
        "R10": st.number_input("R10 Price RWF/kg", value=1200, key="r10"),
        "R12": st.number_input("R12 Price RWF/kg", value=1200, key="r12"),
        "R16": st.number_input("R16 Price RWF/kg", value=1200, key="r16"),
        "R20": st.number_input("R20 Price RWF/kg", value=1200, key="r20"),
        "R25": st.number_input("R25 Price RWF/kg", value=1200, key="r25"),
        "Y32": st.number_input("Y32 Price RWF/kg", value=1350, key="y32"),
        "Y40": st.number_input("Y40 Price RWF/kg", value=1450, key="y40")
    }

    steel_weights = {
        "R6": 0.222, "R8": 0.395, "R10": 0.617, "R12": 0.888,
        "R16": 1.580, "R20": 2.470, "R25": 3.850, "Y32": 6.310, "Y40": 9.860
    }

with col2:
    st.subheader("Cement Types & Concrete Mixes")

    cement_types = {
        "CEM I 32.5N": {"price": 11500, "desc": "General purpose, plastering, masonry"},
        "CEM I 42.5N": {"price": 12500, "desc": "Standard structure, beams, slabs"},
        "CEM I 42.5R": {"price": 13000, "desc": "Rapid hardening, early strength"},
        "CEM I 52.5N": {"price": 14000, "desc": "High strength, bridges, dams"},
        "CEM II 32.5N": {"price": 11000, "desc": "Portland composite, general work"},
        "CEM II 42.5N": {"price": 12000, "desc": "Most common, general structure"}
    }

    selected_cement = st.selectbox(
        "Select Cement Type",
        list(cement_types.keys()),
        index=1,
        help="32.5=Plastering, 42.5=Structure, 52.5=High Strength"
    )

    cement_rate = st.number_input(
        f"{selected_cement} Price RWF/bag 50kg",
        value=cement_types[selected_cement]["price"],
        key="cement"
    )
    st.caption(f"Use: {cement_types[selected_cement]['desc']}")

    mix_ratios = {
        "C10 (1:3:6)": {"cement": 220, "sand": 0.45, "gravel": 0.90},
        "C15 (1:2:4)": {"cement": 300, "sand": 0.42, "gravel": 0.84},
        "C20 (1:1.5:3)": {"cement": 350, "sand": 0.40, "gravel": 0.80},
        "C25 (1:1:2)": {"cement": 450, "sand": 0.35, "gravel": 0.70},
        "C30 (1:1:1.5)": {"cement": 550, "sand": 0.30, "gravel": 0.60},
        "C35 (1:1:1)": {"cement": 650, "sand": 0.25, "gravel": 0.50}
    }

    selected_mix = st.selectbox("Select Concrete Grade", list(mix_ratios.keys()), key="mix", index=2)
    sand_rate = st.number_input("Sand Price RWF/m³", value=25000, key="sand")
    gravel_rate = st.number_input("Gravel Price RWF/m³", value=30000, key="gravel")

    concrete_mix = mix_ratios[selected_mix]

# ========== 3. DIMENSIONS - FIX NAMEERROR + AUTO SCAN ==========
st.header("3. DIMENSIONS")

uploaded_file = st.file_uploader("Upload Plan PDF/Image", type=["pdf","png","jpg","jpeg"])

auto_dimensions = {"length": 0, "width": 0, "height": 0}

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                st.success(f"PDF yasomwe. Pages: {len(pdf.pages)}")
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text() or ""
                import re
                numbers = re.findall(r'(\d+[.,]?\d*)\s*(m|mm|cm)', all_text.lower())
                if numbers:
                    st.info(f"Numbers zabonetse: {numbers[:5]}")
                    if len(numbers) >= 1: auto_dimensions["length"] = float(numbers[0][0].replace(',','.'))
                    if len(numbers) >= 2: auto_dimensions["width"] = float(numbers[1][0].replace(',','.'))
        except Exception as e:
            st.error(f"Ikosa PDF: {e}")

    elif uploaded_file.type.startswith('image'):
        try:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            st.success("Image yasomwe na OCR")
            import re
            numbers = re.findall(r'(\d+[.,]?\d*)\s*(m|mm|cm)', text.lower())
            if numbers:
                st.info(f"Numbers zabonetse: {numbers[:5]}")
                if len(numbers) >= 1: auto_dimensions["length"] = float(numbers[0][0].replace(',','.'))
                if len(numbers) >= 2: auto_dimensions["width"] = float(numbers[1][0].replace(',','.'))
        except Exception as e:
            st.error(f"Ikosa OCR: {e}")
else:
    st.info("Upload PDF/Image cyangwa andika manual")

st.subheader("Confirm/Edit Dimensions")
length = st.number_input("Length (m)", value=float(auto_dimensions["length"]), key="len")
width = st.number_input("Width (m)", value=float(auto_dimensions["width"]), key="wid")
height = st.number_input("Height (m)", value=3.0, key="hei")
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

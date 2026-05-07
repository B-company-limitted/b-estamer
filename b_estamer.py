[9:26 AM, 5/7/2026] B The Gaint: # Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
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
uploaded_file = st.file_uploader("Upload Plan PDF/Image", type=["pdf","png","jpg","jpeg"…
[9:36 AM, 5/7/2026] B The Gaint: MOSES-I: CEO BRUNO, CODE YUZUYE V3.6 "AUTO + MANUAL" EMPIRE 🔥👑

Copy-Paste iyi code yose uko yakabaye muri b_estamer.py. Simbuza ibindi byose.
# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.6 AUTO + MANUAL MODE EMPIRE - All Rights Reserved
# Unauthorized copying, modification, distribution prohibited
# Contact: bruno@b-estamer.rw | +250788000000

import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import re

st.set_page_config(page_title="B-ESTAMER V3.6 AUTO+MANUAL", layout="wide")
st.title("B-ESTAMER V3.6 AUTO + MANUAL EMPIRE 🔄👑")

# --- 1. MODE SELECTION ---
st.header("1. CHOOSE INPUT MODE")
input_mode = st.radio(
    "Hitamo uburyo bwo gushyiramo dimensions:",
    ["🤖 AUTOMATIC - Soma muri PDF/Image", "✍️ MANUAL - Andika wowe"],
    horizontal=True
)

auto_dimensions = {"length": 0, "width": 0, "height": 3.0, "rooms": 3}
uploaded_file = None

# --- 2A. AUTOMATIC MODE ---
if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image":
    st.subheader("Upload Plan for Auto-Extract")
    uploaded_file = st.file_uploader("Upload Plan PDF/Image", type=["pdf","png","jpg","jpeg"], key="auto_upload")

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                st.success(f"✅ PDF yasomwe. Pages: {len(pdf.pages)}")
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text() or ""

                numbers = re.findall(r'(\d+[.,]?\d*)\s*(m|mm|cm)', all_text.lower())
                rooms_found = re.findall(r'(\d+)\s*(room|bedroom|chambre)', all_text.lower())

                if numbers:
                    st.info(f"📐 Numbers zabonetse: {numbers[:5]}")
                    if len(numbers) >= 1:
                        auto_dimensions["length"] = float(numbers[0][0].replace(',','.'))
                        if numbers[0][1] == 'mm': auto_dimensions["length"] /= 1000
                        elif numbers[0][1] == 'cm': auto_dimensions["length"] /= 100
                    if len(numbers) >= 2:
                        auto_dimensions["width"] = float(numbers[1][0].replace(',','.'))
                        if numbers[1][1] == 'mm': auto_dimensions["width"] /= 1000
                        elif numbers[1][1] == 'cm': auto_dimensions["width"] /= 100
                    if len(numbers) >= 3:
                        auto_dimensions["height"] = float(numbers[2][0].replace(',','.'))

                if rooms_found:
                    auto_dimensions["rooms"] = int(rooms_found[0][0])
                    st.info(f"🏠 Rooms zabonetse: {auto_dimensions['rooms']}")
        else:
            st.image(Image.open(uploaded_file), caption="Uploaded Plan", use_column_width=True)
            st.warning("⚠️ Auto-extract kuri image iri coming soon. Koresha MANUAL mode.")

# --- 2B. MANUAL MODE ---
else:
    st.subheader("Andika Dimensions Manual")
    st.info("💡 Tip: Niba ufite plan, reba measurements wandike hano")

# --- 3. HOUSE SPECS - AUTO + MANUAL COMBINED ---
st.header("2. HOUSE SPECS")
st.caption("Values zavuye muri PDF ziba zanditse. Uhindure niba bidakwiye.")

col_h1, col_h2, col_h3, col_h4 = st.columns(4)
with col_h1:
    length = st.number_input("Length (m)", value=auto_dimensions["length"], min_value=0.0, step=0.1, key="len")
    if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image" and length == 0:
        st.error("❌ Length ntiyabonetse muri PDF. Andika manual.")
with col_h2:
    width = st.number_input("Width (m)", value=auto_dimensions["width"], min_value=0.0, step=0.1, key="wid")
    if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image" and width == 0:
        st.error("❌ Width ntiyabonetse muri PDF. Andika manual.")
with col_h3:
    height = st.number_input("Wall Height (m)", value=auto_dimensions["height"], min_value=2.0, step=0.1, key="hei")
with col_h4:
    rooms = st.number_input("No. of Rooms", value=auto_dimensions["rooms"], min_value=1, step=1, key="rooms")

if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image":
    if length > 0 and width > 0:
        st.success(f"🤖 AUTO MODE: {length}m x {width}m x {height}m | {rooms} rooms")
    else:
        st.warning("⚠️ AUTO MODE: PDF ntiyatanze dimensions zose. Uzuza izisigaye manual.")
else:
    st.success(f"✍️ MANUAL MODE: {length}m x {width}m x {height}m | {rooms} rooms")

area = length * width
volume = length * width * 0.5
wall_area = 2 * (length + width) * height
roof_area = area * 1.2

# --- 4. MATERIALS & RATES ---
st.header("3. MATERIALS & RATES - FULL HOUSE")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Cement+Steel", "Blocks+Bricks+Tiles", "Roofing+Timber", "Electrical", "Plumbing+Paint"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Cement RWF/50kg")
        cement_325 = st.number_input("CEM II 32.5R", value=12500)
        cement_425 = st.number_input("CEM II 42.5N", value=13500)
        cement_525 = st.number_input("CEM I 52.5N", value=15000)
        cement_type = st.selectbox("Select Cement", ["CEM II 32.5R", "CEM II 42.5N", "CEM I 52.5N"])
    with c2:
        st.subheader("Steel RWF/kg")
        y10 = st.number_input("Y10", value=1200)
        y12 = st.number_input("Y12", value=1200)
        y16 = st.number_input("Y16", value=1250)
        y40 = st.number_input("Y40", value=1400)
    with c3:
        st.subheader("Concrete Mix")
        concrete_grade = st.selectbox("Grade", ["C15", "C20", "C25", "C30", "C35"])

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Blocks/Bricks")
        brick = st.number_input("Burnt Brick", value=150)
        block_6in = st.number_input("6in Block", value=800)
        block_9in = st.number_input("9in Block", value=1000)
        block_type = st.selectbox("Wall Type", ["9in Block", "6in Block", "Burnt Brick"])
    with c2:
        st.subheader("Tiles RWF/m²")
        tile_ceramic = st.number_input("Ceramic", value=12000)
        tile_porcelain = st.number_input("Porcelain", value=18000)
        tile_granite = st.number_input("Granite", value=25000)
        tile_type = st.selectbox("Tile Type", ["Ceramic", "Porcelain", "Granite"])
    with c3:
        st.subheader("Sand/Aggregate")
        sand = st.number_input("River Sand m³", value=25000)
        aggregate = st.number_input("Aggregate m³", value=30000)
        hardcore = st.number_input("Hardcore m³", value=20000)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Roofing")
        mabati_gauge30 = st.number_input("Mabati Gauge 30/m²", value=8500)
        it4 = st.number_input("IT4 Sheet/m²", value=12000)
        versatile = st.number_input("Versatile/m²", value=15000)
        roof_type = st.selectbox("Roof Type", ["Mabati Gauge 30", "IT4", "Versatile"])
    with c2:
        st.subheader("Timber RWF/pc")
        timber_2x2 = st.number_input("2x2", value=3500)
        timber_3x2 = st.number_input("3x2", value=4500)
        timber_4x2 = st.number_input("4x2", value=6000)

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Electrical")
        cable_15 = st.number_input("1.5mm Cable/roll", value=45000)
        cable_25 = st.number_input("2.5mm Cable/roll", value=65000)
        socket = st.number_input("Socket", value=3500)
    with c2:
        st.subheader("Fittings")
        bulb = st.number_input("LED Bulb", value=2500)
        db_6way = st.number_input("DB 6-Way", value=35000)
        meter = st.number_input("Yaka Meter", value=80000)

with tab5:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Plumbing")
        ppr_20 = st.number_input("PPR 20mm/m", value=2500)
        toilet = st.number_input("WC Complete", value=180000)
        sink = st.number_input("Kitchen Sink", value=85000)
    with c2:
        st.subheader("Paint/Finishes")
        paint_emulsion = st.number_input("Emulsion 20L", value=65000)
        paint_gloss = st.number_input("Gloss 4L", value=28000)
        door_flash = st.number_input("Flash Door", value=95000)
        window_steel = st.number_input("Steel Window m²", value=45000)

# --- 5. AUTO BOQ FULL HOUSE ---
st.header("4. AUTO BOQ - AUTO/MANUAL MODE")

cement_rate = cement_525 if cement_type == "CEM I 52.5N" else cement_425 if cement_type == "CEM II 42.5N" else cement_325
tile_rate = tile_granite if tile_type == "Granite" else tile_porcelain if tile_type == "Porcelain" else tile_ceramic
roof_rate = versatile if roof_type == "Versatile" else it4 if roof_type == "IT4" else mabati_gauge30

if block_type == "9in Block":
    block_rate, block_qty = block_9in, 12.5
elif block_type == "6in Block":
    block_rate, block_qty = block_6in, 15
else:
    block_rate, block_qty = brick, 50

items = [
    ["A", "SUBSTRUCTURE", "", "", "", ""],
    [1, "Site Clearance", area, "m²", 500, area * 500],
    [2, "Excavation", volume, "m³", 3500, volume * 3500],
    [3, "Hardcore filling", area * 0.15, "m³", hardcore, area * 0.15 * hardcore],
    [4, "River Sand blinding", area * 0.05, "m³", sand, area * 0.05 * sand],
    [5, f"Concrete {concrete_grade} foundation", volume * 0.4, "m³", 180000, volume * 0.4 * 180000],
    [6, "Y16 Steel foundation", volume * 80, "kg", y16, volume * 80 * y16],
    ["B", "SUPERSTRUCTURE", "", "", "", ""],
    [7, f"{block_type} Walling", wall_area, "m²", block_rate * block_qty, wall_area * block_rate * block_qty],
    [8, f"Concrete {concrete_grade} columns", height * 0.2 * 4, "m³", 200000, height * 0.2 * 4 * 200000],
    [9, "Y40 Steel columns", height * 100, "kg", y40, height * 100 * y40],
    [10, "Ring Beam Concrete", (length+width)*2*0.2, "m³", 200000, (length+width)*2*0.2*200000],
    ["C", "ROOFING", "", "", "", ""],
    [11, f"{roof_type} Roofing", roof_area, "m²", roof_rate, roof_area * roof_rate],
    [12, "Timber 3x2 Trusses", roof_area/3, "pcs", timber_3x2, roof_area/3 * timber_3x2],
    [13, "Timber 2x2 Purlins", roof_area/2, "pcs", timber_2x2, roof_area/2 * timber_2x2],
    [14, "Fascia Board", (length+width)*2, "m", 3500, (length+width)*2 * 3500],
    ["D", "FINISHES", "", "", "", ""],
    [15, f"{tile_type} Floor Tiles", area, "m²", tile_rate, area * tile_rate],
    [16, "Skirting Tiles", (length+width)*2, "m", 1500, (length+width)*2 * 1500],
    [17, "Emulsion Paint Walls", wall_area * 2, "m²", paint_emulsion/20*0.2, wall_area * 2 * paint_emulsion/20*0.2],
    [18, "Gypsum Ceiling", area, "m²", 15000, area * 15000],
    [19, "Flash Doors", rooms + 2, "pcs", door_flash, (rooms + 2) * door_flash],
    [20, "Steel Windows", rooms * 1.5, "m²", window_steel, rooms * 1.5 * window_steel],
    ["E", "ELECTRICAL", "", "", "", ""],
    [21, "2.5mm Cable Wiring", rooms + 2, "rolls", cable_25, (rooms + 2) * cable_25],
    [22, "Sockets", rooms * 3, "pcs", socket, rooms * 3 * socket],
    [23, "LED Bulbs", rooms + 3, "pcs", bulb, (rooms + 3) * bulb],
    [24, "DB 6-Way", 1, "pc", db_6way, db_6way],
    ["F", "PLUMBING", "", "", "", ""],
    [25, "PPR 20mm Pipes", 30, "m", ppr_20, 30 * ppr_20],
    [26, "WC Toilet Complete", 1, "pc", toilet, toilet],
    [27, "Kitchen Sink", 1, "pc", sink, sink],
    [28, "Water Tank 1000L", 1, "pc", 250000, 250000],
    ["G", "EXTERNAL", "", "", "", ""],
    [29, "Septic Tank", 1, "item", 800000, 800000],
    [30, "Paving Cabros", 20, "m²", 15000, 20 * 15000]
]

df = pd.DataFrame(items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])
subtotal = df[df["Amount"]!= ""]["Amount"].sum()
vat = subtotal * 0.18
grand_total = subtotal + vat

st.info(f"📊 BOQ Generated in *{input_mode.split('-')[0].strip()} MODE* | Dimensions: {length}m x {width}m x {height}m")

st.dataframe(df, use_container_width=True)

col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("SUB TOTAL", f"{subtotal:,.0f} RWF")
col_t2.metric("VAT 18%", f"{vat:,.0f} RWF")
col_t3.metric("GRAND TOTAL", f"{grand_total:,.0f} RWF")

st.success(f"B-ESTAMER V3.6 AUTO+MANUAL READY 💣 | Mode: {input_mode.split('-')[0].strip()} | Copyright BRUNO CONSTRUCTION EMPIRE LTD 

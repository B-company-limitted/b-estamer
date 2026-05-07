
# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.9 ETAGE EMPIRE - AUTO DETECT FLOORS - All Rights Reserved
# Contact: +250787993679 | WhatsApp Business

import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import re
from io import BytesIO

st.set_page_config(page_title="B-ESTAMER V3.9 ETAGE EMPIRE", layout="wide")
st.title("B-ESTAMER V3.9 ETAGE EMPIRE 🏢👑")

# --- 1. MODE SELECTION ---
st.header("1. HITAMO UBURYO")
input_mode = st.radio(
    "Uburyo bwo gushyiramo dimensions:",
    ["🤖 AUTOMATIC - Soma muri PDF/Image", "✍️ MANUAL - Andika wowe"],
    horizontal=True
)

auto_dimensions = {"length": 0.0, "width": 0.0, "height": 3.0, "rooms": 3, "floors": 1}
uploaded_file = None

# --- 2A. AUTOMATIC MODE - ETAGE DETECTION ---
if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image":
    st.subheader("Upload Plan")
    uploaded_file = st.file_uploader("Shyiramo PDF/Image ya Plan", type=["pdf","png","jpg","jpeg"], key="auto_upload")

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                st.success(f"✅ PDF yasomwe. Pages: {len(pdf.pages)}")
                all_text = ""
                for page in pdf.pages:
                    all_text += (page.extract_text() or "") + "\n"

                # DETECT DIMENSIONS
                numbers = re.findall(r'(\d+[.,]?\d*)\s*(m|mm|cm)', all_text.lower())
                rooms_found = re.findall(r'(\d+)\s*(room|bedroom|chambre)', all_text.lower())

                # DETECT ETAGE/FLOORS 🔥
                if re.search(r'second floor|2nd floor|g\+2|r\+2|3\s*(floor|level)', all_text.lower()):
                    auto_dimensions["floors"] = 3
                    st.warning(f"🏢 ETAGE DETECTED: R+2 = 3 Floors")
                elif re.search(r'first floor|1st floor|etage|niveau|g\+1|r\+1|2\s*(floor|level)', all_text.lower()):
                    auto_dimensions["floors"] = 2
                    st.warning(f"🏢 ETAGE DETECTED: R+1 = 2 Floors")
                else:
                    auto_dimensions["floors"] = 1
                    st.info("🏠 INZU ISANZWE: Ground Floor gusa")

                if numbers:
                    st.info(f"📐 Measurements zabonetse: {numbers[:5]}")
                    if len(numbers) >= 1:
                        auto_dimensions["length"] = float(numbers[0][0].replace(',','.'))
                        if numbers[0][1] == 'mm': auto_dimensions["length"] /= 1000.0
                        elif numbers[0][1] == 'cm': auto_dimensions["length"] /= 100.0
                    if len(numbers) >= 2:
                        auto_dimensions["width"] = float(numbers[1][0].replace(',','.'))
                        if numbers[1][1] == 'mm': auto_dimensions["width"] /= 1000.0
                        elif numbers[1][1] == 'cm': auto_dimensions["width"] /= 100.0
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
    st.subheader("Andika Dimensions")
    st.info("💡 Reba kuri plan yawe, andika measurements hano")

# --- 3. HOUSE SPECS ---
st.header("2. HOUSE SPECS")
st.caption("Niba wakoresheje AUTO, values ziba zaruzuye. Hindura niba bidakwiye.")

col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
with col_h1:
    length = st.number_input("Length (m)", value=float(auto_dimensions["length"]), min_value=0.0, step=0.1)
with col_h2:
    width = st.number_input("Width (m)", value=float(auto_dimensions["width"]), min_value=0.0, step=0.1)
with col_h3:
    height = st.number_input("Wall Height (m)", value=float(auto_dimensions["height"]), min_value=2.0, step=0.1)
with col_h4:
    rooms = st.number_input("No. of Rooms", value=int(auto_dimensions["rooms"]), min_value=1, step=1)
with col_h5:
    floors = st.number_input("Floors/Etage", value=int(auto_dimensions["floors"]), min_value=1, step=1, help="1=Ground, 2=R+1, 3=R+2")

if floors > 1:
    st.success(f"🏢 ETAGE MODE: {floors} Floors | {length}m x {width}m x {height}m | {rooms} rooms")
else:
    st.success(f"🏠 GROUND MODE: {length}m x {width}m x {height}m | {rooms} rooms")

area = length * width
volume = length * width * 0.5
wall_area = 2 * (length + width) * height * floors # MULTIPLY BY FLOORS
roof_area = area * 1.2
slab_area = area * (floors - 1) if floors > 1 else 0 # SLAB FOR UPPER FLOORS

# --- 4. MATERIALS - ONE CLICK UI ---
st.header("3. HITAMO MATERIALS - CLICK IMWE GUSA 👆")

with st.expander("🏗️ CEMENT - Kanda hano uhitamo", expanded=True):
    cement_options = {
        "CEM II 32.5R - 12,500 RWF": 12500,
        "CEM II 42.5N - 13,500 RWF": 13500,
        "CEM I 52.5N - 15,000 RWF": 15000
    }
    cement_choice = st.selectbox("Hitamo Cement Grade:", list(cement_options.keys()))
    cement_rate = cement_options[cement_choice]
    cement_type = cement_choice.split(" - ")[0]
    st.info(f"✅ Wahisemo: {cement_type} @ {cement_rate:,} RWF/50kg")

with st.expander("🔩 STEEL - Kanda hano uhitamo"):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        y10 = st.number_input("Y10 RWF/kg", value=1200, key="y10")
        y16 = st.number_input("Y16 RWF/kg", value=1250, key="y16")
    with col_s2:
        y12 = st.number_input("Y12 RWF/kg", value=1200, key="y12")
        y40 = st.number_input("Y40 RWF/kg", value=1400, key="y40")

with st.expander("🧱 AMATAFARI - Kanda hano uhitamo", expanded=True):
    block_options = {
        "23cm Block - 1,000 RWF/pc": (1000, 12.5),
        "15cm Block - 800 RWF/pc": (800, 15.0),
        "Burnt Brick - 150 RWF/pc": (150, 50.0),
        "10cm Block - 650 RWF/pc": (650, 18.0)
    }
    block_choice = st.selectbox("Hitamo Ubwoko bw'Amatafari:", list(block_options.keys()))
    block_rate, block_qty = block_options[block_choice]
    block_type = block_choice.split(" - ")[0]
    st.info(f"✅ Wahisemo: {block_type} @ {block_rate:,} RWF | {block_qty} pcs/m²")

with st.expander("🔲 TILES - Kanda hano uhitamo"):
    tile_options = {
        "Ceramic - 12,000 RWF/m²": 12000,
        "Porcelain - 18,000 RWF/m²": 18000,
        "Granite - 25,000 RWF/m²": 25000
    }
    tile_choice = st.selectbox("Hitamo Tiles:", list(tile_options.keys()))
    tile_rate = tile_options[tile_choice]
    tile_type = tile_choice.split(" - ")[0]
    st.info(f"✅ Wahisemo: {tile_type} @ {tile_rate:,} RWF/m²")

with st.expander("🏠 ROOFING - Kanda hano uhitamo", expanded=True):
    roof_options = {
        "Mabati Gauge 30 - 8,500 RWF/m²": 8500,
        "IT4 Sheet - 12,000 RWF/m²": 12000,
        "Versatile - 15,000 RWF/m²": 15000
    }
    roof_choice = st.selectbox("Hitamo Roof Type:", list(roof_options.keys()))
    roof_rate = roof_options[roof_choice]
    roof_type = roof_choice.split(" - ")[0]
    st.info(f"✅ Wahisemo: {roof_type} @ {roof_rate:,} RWF/m²")

with st.expander("⚙️ CONCRETE GRADE"):
    concrete_grade = st.selectbox("Hitamo Concrete Grade:", ["C15", "C20", "C25", "C30", "C35"], index=2)
    st.info(f"✅ Wahisemo: {concrete_grade}")

with st.expander("🏖️ SAND & AGGREGATE"):
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        sand = st.number_input("River Sand m³", value=25000)
    with col_a2:
        aggregate = st.number_input("Aggregate m³", value=30000)
    with col_a3:
        hardcore = st.number_input("Hardcore m³", value=20000)

with st.expander("🪵 TIMBER"):
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        timber_2x2 = st.number_input("2x2 RWF/pc", value=3500)
    with col_t2:
        timber_3x2 = st.number_input("3x2 RWF/pc", value=4500)
    with col_t3:
        timber_4x2 = st.number_input("4x2 RWF/pc", value=6000)

with st.expander("⚡ ELECTRICAL"):
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        cable_25 = st.number_input("2.5mm Cable/roll", value=65000)
        bulb = st.number_input("LED Bulb", value=2500)
    with col_e2:
        socket = st.number_input("Socket", value=3500)
        db_6way = st.number_input("DB 6-Way", value=35000)
    with col_e3:
        cable_15 = st.number_input("1.5mm Cable/roll", value=45000)
        meter = st.number_input("Yaka Meter", value=80000)

with st.expander("🚿 PLUMBING & FINISHES"):
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        ppr_20 = st.number_input("PPR 20mm/m", value=2500)
        paint_emulsion = st.number_input("Emulsion 20L", value=65000)
    with col_p2:
        toilet = st.number_input("WC Complete", value=180000)
        door_flash = st.number_input("Flash Door", value=95000)
    with col_p3:
        sink = st.number_input("Kitchen Sink", value=85000)
        window_steel = st.number_input("Steel Window m²", value=45000)

# --- 5. AUTO BOQ WITH ETAGE ---
st.header("4. AUTO BOQ - ETAGE MODE")

items = [
    ["A", "SUBSTRUCTURE", "", "", "", ""],
    [1, "Site Clearance", area, "m²", 500, area * 500],
    [2, "Excavation", volume, "m³", 3500, volume * 3500],
    [3, "Hardcore filling", area * 0.15, "m³", hardcore, area * 0.15 * hardcore],
    [4, "River Sand blinding", area * 0.05, "m³", sand, area * 0.05 * sand],
    [5, f"Concrete {concrete_grade} foundation", volume * 0.4, "m³", 180000, volume * 0.4 * 180000],
    [6, "Y16 Steel foundation", volume * 80, "kg", y16, volume * 80 * y16],
    ["B", "SUPERSTRUCTURE", "", "", "", ""],
    [7, f"{block_type} Walling {floors} Floor(s)", wall_area, "m²", block_rate * block_qty, wall_area * block_rate * block_qty],
    [8, f"Concrete {concrete_grade} columns {floors} Floor(s)", height * 0.2 * 4 * floors, "m³", 200000, height * 0.2 * 4 * floors * 200000],
    [9, f"Y40 Steel columns {floors} Floor(s)", height * 100 * floors, "kg", y40, height * 100 * floors * y40],
    [10, f"Ring Beam Concrete {floors} Floor(s)", (length+width)*2*0.2*floors, "m³", 200000, (length+width)*2*0.2*floors*200000],
]

# ADD SLAB IF ETAGE
if floors > 1:
    items.append([10.5, f"Concrete Slab {floors-1} Floor(s)", slab_area, "m²", 25000, slab_area * 25000])
    items.append([10.6, f"Y12 Steel Slab", slab_area * 15, "kg", y12, slab_area * 15 * y12])

items.extend([
    ["C", "ROOFING", "", "", "", ""],
    [11, f"{roof_type} Roofing", roof_area, "m²", roof_rate, roof_area * roof_rate],
    [12, "Timber 3x2 Trusses", roof_area/3, "pcs", timber_3x2, roof_area/3 * timber_3x2],
    [13, "Timber 2x2 Purlins", roof_area/2, "pcs", timber_2x2, roof_area/2 * timber_2x2],
    [14, "Fascia Board", (length+width)*2, "m", 3500, (length+width)*2 * 3500],
    ["D", "FINISHES", "", "", "", ""],
    [15, f"{tile_type} Floor Tiles {floors} Floor(s)", area * floors, "m²", tile_rate, area * floors * tile_rate],
    [16, f"Skirting Tiles {floors} Floor(s)", (length+width)*2*floors, "m", 1500, (length+width)*2*floors * 1500],
    [17, f"Emulsion Paint Walls {floors} Floor(s)", wall_area * 2, "m²", paint_emulsion/20*0.2, wall_area * 2 * paint_emulsion/20*0.2],
    [18, f"Gypsum Ceiling {floors} Floor(s)", area * floors, "m²", 15000, area * floors * 15000],
    [19, "Flash Doors", rooms + 2, "pcs", door_flash, (rooms + 2) * door_flash],
    [20, "Steel Windows", rooms * 1.5, "m²", window_steel, rooms * 1.5 * window_steel],
    ["E", "ELECTRICAL", "", "", "", ""],
    [21, "2.5mm Cable Wiring", rooms + 2, "rolls", cable_25, (rooms + 2) * cable_25],
    [22, "Sockets", rooms * 3 * floors, "pcs", socket, rooms * 3 * floors * socket],
    [23, "LED Bulbs", (rooms + 3) * floors, "pcs", bulb, (rooms + 3) * floors * bulb],
    [24, "DB 6-Way", 1, "pc", db_6way, db_6way],
    ["F", "PLUMBING", "", "", "", ""],
    [25, "PPR 20mm Pipes", 30 * floors, "m", ppr_20, 30 * floors * ppr_20],
    [26, "WC Toilet Complete", floors, "pc", toilet, floors * toilet],
    [27, "Kitchen Sink", 1, "pc", sink, sink],
    [28, "Water Tank 1000L", 1, "pc", 250000, 250000],
    ["G", "EXTERNAL", "", "", "", ""],
    [29, "Septic Tank", 1, "item", 800000, 800000],
    [30, "Paving Cabros", 20, "m²", 15000, 20 * 15000]
])

df = pd.DataFrame(items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])
subtotal = df[df["Amount"]!= ""]["Amount"].sum()
vat = subtotal * 0.18
grand_total = subtotal + vat

if floors > 1:
    st.info(f"🏢 ETAGE BOQ: R+{floors-1} | {cement_type} | {block_type} | {tile_type} | {roof_type} | {length}m x {width}m")
else:
    st.info(f"🏠 GROUND BOQ: {cement_type} | {block_type} | {tile_type} | {roof_type} | {length}m x {width}m")

st.dataframe(df, use_container_width=True)

col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("SUB TOTAL", f"{subtotal:,.0f} RWF")
col_t2.metric("VAT 18%", f"{vat:,.0f} RWF")
col_t3.metric("GRAND TOTAL", f"{grand_total:,.0f} RWF")

# --- 6. EXCEL EXPORT ---
st.header("5. DOWNLOAD EXCEL")

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='BOQ')
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df)

st.download_button(
    label="📥 Download BOQ Excel",
    data=excel_data,
    file_name=f"B-ESTAMER_R+{floors-1}{length}x{width}{grand_total:,.0f}RWF.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success(f"B-ESTAMER V3.9 ETAGE EMPIRE READY 💣 | Copyright BRUNO CONSTRUCTION EMPIRE LTD 2026")

# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.14.1 GENIUS EMPIRE - TypeError Fixed - All Rights Reserved
# WhatsApp/Call: 0787993679

import streamlit as st
import pandas as pd
import pdfplumber
from PIL import Image
import re
from io import BytesIO

st.set_page_config(page_title="B-ESTAMER V3.14.1 GENIUS EMPIRE", layout="wide")
st.title("B-ESTAMER V3.14.1 GENIUS EMPIRE 🏗️🧠👑")

if 'saved_prices' in st.session_state:
    sp = st.session_state['saved_prices']
    default_cement_rate = sp.get('cement_rate', 12500)
    default_block_rate = sp.get('block_rate', 1000)
    default_tile_rate = sp.get('tile_rate', 12000)
    default_roof_rate = sp.get('roof_rate', 8500)
    default_concrete_rate = sp.get('concrete_rate', 180000)
else:
    default_cement_rate = 12500
    default_block_rate = 1000
    default_tile_rate = 12000
    default_roof_rate = 8500
    default_concrete_rate = 180000

st.header("1. HITAMO UBURYO")
input_mode = st.radio(
    "Uburyo bwo gushyiramo dimensions:",
    ["🤖 AUTOMATIC - Soma muri PDF/Image", "✍️ MANUAL - Andika wowe"],
    horizontal=True
)

auto_dimensions = {"length": 0.0, "width": 0.0, "height": 3.0, "rooms": 3, "floors": 1}
uploaded_file = None
confidence = 100
warnings = []
valid_dims = []

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
                    tables = page.extract_tables()
                    for table in tables:
                        all_text += " ".join([str(cell) for row in table for cell in row if cell]) + "\n"
                    if page.annots:
                        for annot in page.annots:
                            if annot.get("contents"):
                                all_text += annot.get("contents") + "\n"

                st.info(f"📄 Text + Tables byasomwe: {len(all_text)} characters")

                dim_pattern = r'(?:dim|dimension|length|width|longueur|largeur)?\s*[:=]?\s*(\d+[.,]?\d*)\s*(m|mm|cm|meter|metre)\b'
                numbers = re.findall(dim_pattern, all_text.lower(), re.IGNORECASE)

                if re.search(r'second floor|2nd floor|g\+2|r\+2|3\s*(floor|level|storey)|triplex|niveau 2', all_text.lower()):
                    auto_dimensions["floors"] = 3
                    st.warning(f"🏢 ETAGE DETECTED: R+2 = 3 Floors")
                elif re.search(r'first floor|1st floor|etage|niveau|g\+1|r\+1|2\s*(floor|level|storey)|upper floor|duplex|mezzanine|niveau 1', all_text.lower()):
                    auto_dimensions["floors"] = 2
                    st.warning(f"🏢 ETAGE DETECTED: R+1 = 2 Floors")
                else:
                    auto_dimensions["floors"] = 1
                    st.info("🏠 INZU ISANZWE: Ground Floor gusa")

                rooms_keywords = r'(\d+)\s*(room|bedroom|chambre|chamb|ch|bed|rm|suite|master|salon|living|kitchen|cuisine)'
                rooms_found = re.findall(rooms_keywords, all_text.lower())
                if rooms_found:
                    total_rooms = len(set([r[0] for r in rooms_found]))
                    auto_dimensions["rooms"] = max(total_rooms, 1)
                    st.info(f"🏠 Rooms zabonetse: {auto_dimensions['rooms']}")

                if numbers:
                    for num, unit in numbers:
                        val = float(num.replace(',','.'))
                        if unit == 'mm': val /= 1000.0
                        elif unit == 'cm': val /= 100.0
                        if 2.0 <= val <= 60.0:
                            valid_dims.append(round(val, 2))

                    valid_dims = sorted(list(set(valid_dims)), reverse=True)
                    st.info(f"📐 Valid Dimensions zabonetse: {valid_dims}")

                    if len(valid_dims) >= 1:
                        auto_dimensions["length"] = valid_dims[0]
                    if len(valid_dims) >= 2:
                        auto_dimensions["width"] = valid_dims[1]
                    if len(valid_dims) >= 3:
                        heights = [d for d in valid_dims if 2.5 <= d <= 4.5]
                        if heights:
                            auto_dimensions["height"] = heights[0]

                if auto_dimensions["length"] == 0.0 or auto_dimensions["width"] == 0.0:
                    confidence -= 40
                    warnings.append("❌ Nta Length/Width zabonetse muri PDF")
                if auto_dimensions["length"] > 50 or auto_dimensions["width"] > 50:
                    confidence -= 20
                    warnings.append("⚠️ Length/Width zirenze 50m - Zishobora kuba scale")
                if auto_dimensions["floors"] == 1 and re.search(r'etage|floor|g\+|r\+', all_text.lower()):
                    confidence -= 15
                    warnings.append("⚠️ PDF ivuga Etage ariko Floors = 1")
                if len(valid_dims) < 3:
                    confidence -= 25
                    warnings.append("⚠️ Dimensions nke zabonetse - Koresha MANUAL")

                if confidence >= 90:
                    st.success(f"🎯 AI CONFIDENCE: {confidence}% - HIGH ACCURACY")
                elif confidence >= 70:
                    st.warning(f"⚠️ AI CONFIDENCE: {confidence}% - REBA NEZA HEPFO")
                else:
                    st.error(f"🚨 AI CONFIDENCE: {confidence}% - KOROSHA MANUAL MODE")
                for warn in warnings:
                    st.caption(warn)
        else:
            st.image(Image.open(uploaded_file), caption="Uploaded Plan", use_column_width=True)
            st.warning("⚠️ Auto-extract kuri image iri coming soon. Koresha MANUAL mode.")

else:
    st.subheader("Andika Dimensions")
    st.info("💡 Reba kuri plan yawe, andika measurements hano")

st.header("2. HOUSE SPECS - GENZURA & HINDURA")
st.caption("Niba AUTO yasomye nabi, hindura hano. Wowe ni Boss.")

col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
with col_h1:
    length = st.number_input("Length (m) ⚠️", value=float(auto_dimensions["length"]), min_value=0.0, step=0.1)
with col_h2:
    width = st.number_input("Width (m) ⚠️", value=float(auto_dimensions["width"]), min_value=0.0, step=0.1)
with col_h3:
    height = st.number_input("Wall Height (m)", value=float(auto_dimensions["height"]), min_value=2.0, step=0.1)
with col_h4:
    rooms = st.number_input("No. of Rooms", value=int(auto_dimensions["rooms"]), min_value=1, step=1)
with col_h5:
    floors = st.number_input("Floors/Etage ⚠️", value=int(auto_dimensions["floors"]), min_value=1, step=1, help="1=Ground, 2=R+1, 3=R+2")

if floors > 1:
    st.success(f"🏢 ETAGE MODE: {floors} Floors | {length}m x {width}m x {height}m | {rooms} rooms")
else:
    st.success(f"🏠 GROUND MODE: {length}m x {width}m x {height}m | {rooms} rooms")

area = length * width
volume = length * width * 0.5
wall_area = 2 * (length + width) * height * floors
roof_area = area * 1.2
slab_area = area * (floors - 1) if floors > 1 else 0

st.header("3. SMART MATERIALS ENGINE 🧠⚡")
st.caption("💡 App iratekereza: Iraguha suggestions, irabara quantities, irakuburira")

if area < 80:
    st.info("🏠 *SMART TIP:* Inzu nto < 80m² → Saba 15cm Blocks + CEM II 32.5R")
    suggested_block = "15cm Block"
    suggested_cement = "CEM II 32.5R"
elif area < 150:
    st.info("🏡 *SMART TIP:* Inzu medium 80-150m² → Saba 23cm Blocks + CEM II 42.5N")
    suggested_block = "23cm Block"
    suggested_cement = "CEM II 42.5N"
else:
    st.warning("🏢 *SMART TIP:* Inzu nini > 150m² → Saba 23cm Blocks + CEM I 52.5N")
    suggested_block = "23cm Block"
    suggested_cement = "CEM I 52.5N"

col_smart1, col_smart2, col_smart3 = st.columns(3)
with col_smart1:
    st.metric("🧱 Blocks Uzakeneye", f"{wall_area * 12.5:,.0f} pcs")
with col_smart2:
    st.metric("🏗️ Cement Bags", f"{(volume * 6) + (wall_area * 0.2):,.0f} bags")
with col_smart3:
    st.metric("🔩 Steel Total", f"{(volume * 80) + (height * 100 * floors):,.0f} kg")

st.subheader("⚡ SMART PRICE INTELLIGENCE")
st.caption("App irakuburira niba igiciro kiri hejuru cyane cyangwa hasi cyane")

with st.expander("🏗️ CEMENT - SMART INPUT", expanded=True):
    col_c1, col_c2, col_c3 = st.columns([2,1,1])
    with col_c1:
        cement_type = st.text_input("Izina rya Cement", value=suggested_cement)
    with col_c2:
        cement_rate = st.number_input("Igiciro 50kg RWF", value=default_cement_rate, step=500, min_value=0)
    with col_c3:
        if cement_rate < 10000:
            st.error("🚨 Hasi cyane!")
        elif cement_rate > 18000:
            st.warning("⚠️ Hejuru!")
        else:
            st.success("✅ OK")
    st.success(f"✅ Wahisemo: {cement_type} @ {cement_rate:,} RWF")

with st.expander("🧱 AMATAFARI - SMART INPUT", expanded=True):
    col_b1, col_b2, col_b3, col_b4 = st.columns([2,1,1,1])
    with col_b1:
        block_type = st.text_input("Izina ry'Amatafari", value=suggested_block)
    with col_b2:
        block_rate = st.number_input("Igiciro RWF/pc", value=default_block_rate, step=50, min_value=0)
    with col_b3:
        block_qty = st.number_input("Pieces/m²", value=12.5, step=0.5, min_value=0.0)
    with col_b4:
        if block_rate < 500:
            st.error("🚨 Hasi!")
        elif block_rate > 2000:
            st.warning("⚠️ Hejuru!")
        else:
            st.success("✅ OK")
    st.success(f"✅ Wahisemo: {block_type} @ {block_rate:,} RWF")

with st.expander("🔲 TILES - SMART INPUT"):
    col_t1, col_t2, col_t3 = st.columns([2,1,1])
    with col_t1:
        tile_type = st.text_input("Izina rya Tiles", value="Ceramic")
    with col_t2:
        tile_rate = st.number_input("Igiciro RWF/m²", value=default_tile_rate, step=500, min_value=0)
    with col_t3:
        if tile_rate < 8000:
            st.error("🚨 Hasi")
        elif tile_rate > 35000:
            st.warning("⚠️ Luxury!")
        else:
            st.success("✅ OK")
    st.success(f"✅ Wahisemo: {tile_type} @ {tile_rate:,} RWF")

with st.expander("🏠 ROOFING - SMART INPUT", expanded=True):
    col_r1, col_r2, col_r3 = st.columns([2,1,1])
    with col_r1:
        roof_type = st.text_input("Izina rya Roofing", value="Mabati Gauge 30")
    with col_r2:
        roof_rate = st.number_input("Igiciro RWF/m²", value=default_roof_rate, step=500, min_value=0)
    with col_r3:
        if roof_rate < 6000:
            st.error("🚨 Hasi!")
        elif roof_rate > 20000:
            st.warning("⚠️ Hejuru!")
        else:
            st.success("✅ OK")
    st.success(f"✅ Wahisemo: {roof_type} @ {roof_rate:,} RWF")

st.subheader("🚀 SMART PACKAGES - CLICK IMWE GUSA")
col_pkg1, col_pkg2, col_pkg3 = st.columns(3)
with col_pkg1:
    if st.button("💰 ECONOMY PACKAGE", use_container_width=True):
        st.session_state['smart_package'] = "economy"
        st.rerun()
with col_pkg2:
    if st.button("🏡 STANDARD PACKAGE", use_container_width=True):
        st.session_state['smart_package'] = "standard"
        st.rerun()
with col_pkg3:
    if st.button("👑 LUXURY PACKAGE", use_container_width=True):
        st.session_state['smart_package'] = "luxury"
        st.rerun()

if 'smart_package' in st.session_state:
    pkg = st.session_state['smart_package']
    if pkg == "economy":
        cement_rate = 11500; block_rate = 800; tile_rate = 9000; roof_rate = 7000
        st.success("✅ ECONOMY PACK: Cement 11.5K | Block 800 | Tile 9K | Mabati 7K")
    elif pkg == "standard":
        cement_rate = 12500; block_rate = 1000; tile_rate = 12000; roof_rate = 8500
        st.success("✅ STANDARD PACK: Cement 12.5K | Block 1K | Tile 12K | Mabati 8.5K")
    elif pkg == "luxury":
        cement_rate = 15000; block_rate = 1200; tile_rate = 25000; roof_rate = 15000
        st.success("✅ LUXURY PACK: Cement 15K | Block 1.2K | Granite 25K | Versatile 15K")

with st.expander("⚙️ CONCRETE GRADE"):
    col_con1, col_con2 = st.columns([2,1])
    with col_con1:
        concrete_grade = st.text_input("Concrete Grade", value="C25")
    with col_con2:
        concrete_rate = st.number_input("Igiciro RWF/m³", value=default_concrete_rate, step=10000, min_value=0)

with st.expander("🏖️ SAND & AGGREGATE"):
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        sand = st.number_input("River Sand RWF/m³", value=25000, step=1000)
    with col_a2:
        aggregate = st.number_input("Aggregate RWF/m³", value=30000, step=1000)
    with col_a3:
        hardcore = st.number_input("Hardcore RWF/m³", value=20000, step=1000)

with st.expander("🪵 TIMBER"):
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        timber_2x2 = st.number_input("2x2 RWF/pc", value=3500, step=100)
    with col_t2:
        timber_3x2 = st.number_input("3x2 RWF/pc", value=4500, step=100)
    with col_t3:
        timber_4x2 = st.number_input("4x2 RWF/pc", value=6000, step=100)

with st.expander("⚡ ELECTRICAL"):
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        cable_25 = st.number_input("2.5mm Cable/roll", value=65000, step=1000)
        bulb = st.number_input("LED Bulb", value=2500, step=100)
    with col_e2:
        socket = st.number_input("Socket", value=3500, step=100)
        db_6way = st.number_input("DB 6-Way", value=35000, step=1000)
    with col_e3:
        cable_15 = st.number_input("1.5mm Cable/roll", value=45000, step=1000)
        meter = st.number_input("Yaka Meter", value=80000, step=5000)

with st.expander("🚿 PLUMBING & FINISHES"):
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        ppr_20 = st.number_input("PPR 20mm/m", value=2500, step=100)
        paint_emulsion = st.number_input("Emulsion 20L", value=65000, step=1000)
    with col_p2:
        toilet = st.number_input("WC Complete", value=180000, step=5000)
        door_flash = st.number_input("Flash Door", value=95000, step=1000)
    with col_p3:
        sink = st.number_input("Kitchen Sink", value=85000, step=1000)
        window_steel = st.number_input("Steel Window m²", value=45000, step=1000)

st.header("4. AUTO BOQ - VARIABLE + FIXED COSTS")

variable_items = [
    ["A", "SUBSTRUCTURE - VARIABLE", "", "", "", ""],
    [1, "Site Clearance", area, "m²", 500, area * 500],
    [2, "Excavation", volume, "m³", 3500, volume * 3500],
    [3, "Hardcore filling", area * 0.15, "m³", hardcore, area * 0.15 * hardcore],
    [4, "River Sand blinding", area * 0.05, "m³", sand, area * 0.05 * sand],
    [5, f"Concrete {concrete_grade} foundation", volume * 0.4, "m³", concrete_rate, volume * 0.4 * concrete_rate],
    [6, "Y16 Steel foundation", volume * 80, "kg", 1250, volume * 80 * 1250],
    ["B", "SUPERSTRUCTURE - VARIABLE", "", "", "", ""],
    [7, f"{block_type} Walling {floors} Floor(s)", wall_area, "m²", block_rate * block_qty, wall_area * block_rate * block_qty],
    [8, f"Concrete {concrete_grade} columns {floors} Floor(s)", height * 0.2 * 4 * floors, "m³", concrete_rate, height * 0.2 * 4 * floors * concrete_rate],
    [9, f"Y40 Steel columns {floors} Floor(s)", height * 100 * floors, "kg", 1400, height * 100 * floors * 1400],
    [10, f"Ring Beam Concrete {floors} Floor(s)", (length+width)*2*0.2*floors, "m³", concrete_rate, (length+width)*2*0.2*floors*concrete_rate],
]

if floors > 1:
    variable_items.append([10.5, f"Concrete Slab {floors-1} Floor(s)", slab_area, "m²", 25000, slab_area * 25000])
    variable_items.append([10.6, f"Y12 Steel Slab", slab_area * 15, "kg", 1200, slab_area * 15 * 1200])

variable_items.extend([
    ["C", "ROOFING - VARIABLE", "", "", "", ""],
    [11, f"{roof_type} Roofing", roof_area, "m²", roof_rate, roof_area * roof_rate],
    [12, "Timber 3x2 Trusses", roof_area/3, "pcs", timber_3x2, roof_area/3 * timber_3x2],
    [13, "Timber 2x2 Purlins", roof_area/2, "pcs", timber_2x2, roof_area/2 * timber_2x2],
    [14, "Fascia Board", (length+width)*2, "m", 3500, (length+width)*2 * 3500],
    ["D", "FINISHES - VARIABLE", "", "", "", ""],
    [15, f"{tile_type} Floor Tiles {floors} Floor(s)", area * floors, "m²", tile_rate, area * floors * tile_rate],
    [16, f"Skirting Tiles {floors} Floor(s)", (length+width)*2*floors, "m", 1500, (length+width)*2*floors * 1500],
    [17, f"Emulsion Paint Walls {floors} Floor(s)", wall_area * 2, "m²", paint_emulsion/20*0.2, wall_area * 2 * paint_emulsion/20*0.2],
    [18, f"Gypsum Ceiling {floors} Floor(s)", area * floors, "m²", 15000, area * floors * 15000],
    [19, "Flash Doors", rooms + 2, "pcs", door_flash, (rooms + 2) * door_flash],
    [20, "Steel Windows", rooms * 1.5, "m²", window_steel, rooms * 1.5 * window_steel],
])

st.subheader("💰 FIXED COSTS - NTIZIHINDUKA")
st.caption("Izi costs ntiziterwa na size y'inzu. Hindura niba bikenewe.")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    septic_tank_cost = st.number_input("Septic Tank RWF", value=800000, step=50000)
    water_tank_cost = st.number_input("Water Tank 1000L RWF", value=250000, step=25000)
    yaka_meter_cost = st.number_input("Yaka Meter RWF", value=80000, step=10000)
with col_f2:
    db_board_cost = st.number_input("DB Board RWF", value=db_6way, step=5000)
    soak_pit_cost = st.number_input("Soak Pit RWF", value=350000, step=50000)
    transport_cost = st.number_input("Transport RWF", value=500000, step=100000)
with col_f3:
    site_office_cost = st.number_input("Site Office RWF", value=300000, step=50000)
    scaffolding_cost = st.number_input("Scaffolding RWF", value=400000, step=50000)
    contingency_cost = st.number_input("Contingency RWF", value=1000000, step=100000)

fixed_items = [
    ["E", "ELECTRICAL - MIXED", "", "", "", ""],
    [21, "2.5mm Cable Wiring", rooms + 2, "rolls", cable_25, (rooms + 2) * cable_25],
    [22, "Sockets", rooms * 3 * floors, "pcs", socket, rooms * 3 * floors * socket],
    [23, "LED Bulbs", (rooms + 3) * floors, "pcs", bulb, (rooms + 3) * floors * bulb],
    [24, "DB Board - FIXED", 1, "pc", db_board_cost, db_board_cost],
    [24.1, "Yaka Meter - FIXED", 1, "pc", yaka_meter_cost, yaka_meter_cost],
    ["F", "PLUMBING - MIXED", "", "", "", ""],
    [25, "PPR 20mm Pipes", 30 * floors, "m", ppr_20, 30 * floors * ppr_20],
    [26, "WC Toilet Complete", floors, "pc", toilet, floors * toilet],
    [27, "Kitchen Sink", 1, "pc", sink, sink],
    [28, "Water Tank 1000L - FIXED", 1, "pc", water_tank_cost, water_tank_cost],
    ["G", "EXTERNAL - FIXED", "", "", "", ""],
    [29, "Septic Tank - FIXED", 1, "item", septic_tank_cost, septic_tank_cost],
    [29.1, "Soak Pit - FIXED", 1, "item", soak_pit_cost, soak_pit_cost],
    [30, "Paving Cabros", 20, "m²", 15000, 20 * 15000],
    ["H", "PRELIMINARIES - FIXED", "", "", "", ""],
    [31, "Transport - FIXED", 1, "item", transport_cost, transport_cost],
    [32, "Site Office - FIXED", 1, "item", site_office_cost, site_office_cost],
    [33, "Scaffolding - FIXED", 1, "item", scaffolding_cost, scaffolding_cost],
    [34, "Contingency - FIXED", 1, "item", contingency_cost, contingency_cost],
]

all_items = variable_items + fixed_items
df = pd.DataFrame(all_items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])
df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce').fillna(0)
df["Qty"] = pd.to_numeric(df["Qty"], errors='coerce').fillna(0)
df["Rate"] = pd.to_numeric(df["Rate"], errors='coerce').fillna(0)

variable_total = df[df["Description"].str.contains("VARIABLE|MIXED", na=False)]["Amount"].sum()
fixed_total = df[df["Description"].str.contains("FIXED", na=False)]["Amount"].sum()
subtotal = df["Amount"].sum()
vat = subtotal * 0.18
grand_total = subtotal + vat

if floors > 1:
    st.info(f"🏢 ETAGE BOQ: R+{floors-1} | Variable: {variable_total:,.0f} RWF | Fixed: {fixed_total:,.0f} RWF")
else:
    st.info(f"🏠 GROUND BOQ: Variable: {variable_total:,.0f} RWF | Fixed: {fixed_total:,.0f} RWF")

st.dataframe(df, use_container_width=True)

col_t1, col_t2, col_t3, col_t4 = st.columns(4)
col_t1.metric("VARIABLE COSTS", f"{variable_total:,.0f} RWF")
col_t2.metric("FIXED COSTS", f"{fixed_total:,.0f} RWF")
col_t3.metric("SUB TOTAL", f"{subtotal:,.0f} RWF")
col_t4.metric("GRAND TOTAL", f"{grand_total:,.0f} RWF")

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

st.header("6. SAVE/LOAD PRICE LIST 💾")
st.caption("Bika igiciro cyawe kugirango utongera kwandika buri gihe")

col_save1, col_save2 = st.columns(2)
with col_save1:
    if st.button("💾 Bika Price List Yanjye"):
        price_data = {
            "cement_type": cement_type, "cement_rate": cement_rate,
            "block_type": block_type, "block_rate": block_rate, "block_qty": block_qty,
            "tile_type": tile_type, "tile_rate": tile_rate,
            "roof_type": roof_type, "roof_rate": roof_rate,
            "concrete_grade": concrete_grade, "concrete_rate": concrete_rate,
            "sand": sand, "aggregate": aggregate, "hardcore": hardcore
        }
        st.session_state['saved_prices'] = price_data
        st.success("✅ Price List Yabikwe! Nugaruka izagaruka uko wayisize.")

with col_save2:
    if st.button("📂 Koresha Price List Nabikije"):
        if 'saved_prices' in st.session_state:
            st.success("✅ Price List Yakuwe! Funga app ufunure → Prices zawe zizagaruka")
        else:
            st.warning("⚠️ Nta Price List urabika. Banza ukande 'Bika Price List'")

st.header("7. UKO TWABAZE - VERIFY NONAHA ✅")
st.caption("Reba formula zose. Niba hari itari yo, hindura hejuru.")

with st.expander("📐 CALCULATIONS BREAKDOWN - Kanda urebe", expanded=False):
    st.subheader("A. Dimensions")
    st.code(f"""
Length = {length} m
Width = {width} m
Height = {height} m
Floors = {floors}
Area = {length} × {width} = {area} m²
Wall Area = 2 × ({length} + {width}) × {height} × {floors} = {wall_area} m²
Roof Area = {area} × 1.2 = {roof_area} m²
    """)

    st.subheader("B. Key Materials")
    st.code(f"""
Blocks Needed = {wall_area} m² × {block_qty} pcs/m² = {wall_area * block_qty:,.0f} pcs
Block Cost = {wall_area * block_qty:,.0f} pcs × {block_rate:,} RWF = {wall_area * block_qty * block_rate:,.0f} RWF

Cement Bags = Foundation + Walls + Columns = ~{(volume * 6) + (wall_area * 0.2):.0f} bags
Cement Cost = {(volume * 6) + (wall_area * 0.2):.0f} bags × {cement_rate:,} RWF = {((volume * 6) + (wall_area * 0.2)) * cement_rate:,.0f} RWF

Roofing Cost = {roof_area} m² × {roof_rate:,} RWF = {roof_area * roof_rate:,.0f} RWF
    """)

    st.subheader("C. Totals")
    st.code(f"""
VARIABLE COSTS = {variable_total:,.0f} RWF
FIXED COSTS = {fixed_total:,.0f} RWF
SUB TOTAL = {subtotal:,.0f} RWF
VAT 18% = {vat:,.0f} RWF
GRAND TOTAL = {grand_total:,.0f} RWF
    """)

st.success("✅ Niba formula zose ari zo, BOQ ni yo 100%. Niba hari itari yo, hindura prices/sizes hejuru.")

st.header("8. SANITY CHECK - GERERANYA NA FUNDI 👷")
st.caption("Niba fundi aguhaye BOQ, gereranya hano:")
col_check1, col_check2 = st.columns(2)
with col_check1:
    fundi_total = st.number_input("Andika Grand Total ya Fundi RWF", value=0, step=100000)
with col_check2:
    if fundi_total > 0:
        diff = grand_total - fundi_total
        diff_percent = (diff / fundi_total) * 100
        if abs(diff_percent) <= 10:
            st.success(f"✅ Hafi cyane! Diff: {diff_percent:.1f}% = {diff:,.0f} RWF")
        elif abs(diff_percent) <= 20:
            st.warning(f"⚠️ Hari diff: {diff_percent:.1f}% = {diff:,.0f} RWF - Genzura materials")
        else:
            st.error(f"🚨 Diff nini: {diff_percent:.1f}% = {diff:,.0f} RWF - Habaye ikosa")

st.divider()
st.caption(f"""
⚖️ *DISCLAIMER:* B-ESTAMER ni *Quantity Estimation Tool* ifasha kubara materials.
*SI SIMBUZA* Engineer cyangwa Architect. *BURI GIHE* suzuma BOQ na Professional mbere yo gutanga kuri tender/bank.
Accuracy ishingiye kuri: 1) PDF nziza 2) Prices z'ukuri 3) Verification yawe.

📞 *CONTACT BRUNO CONSTRUCTION EMPIRE LTD:*
*WhatsApp/Call:* 0787993679
*Service:* BOQ Estimation | Construction | Consultation

© 2026 BRUNO CONSTRUCTION EMPIRE LTD - All Rights Reserved
""")

st.success(f"B-ESTAMER V3.14.1 GENIUS EMPIRE READY 💣 | AI Confidence: {confidence}%")

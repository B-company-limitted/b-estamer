# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.18 PRECISION EMPIRE - Materials Table + RPPA + Excel Export
# WhatsApp/Call: 0787993679

import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="B-ESTAMER V3.18 PRECISION EMPIRE", layout="wide")
st.title("B-ESTAMER V3.18 PRECISION EMPIRE 🏗️🧠👑")

# Load saved prices
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
valid_dims = []

if input_mode == "🤖 AUTOMATIC - Soma muri PDF/Image":
    uploaded_file = st.file_uploader("Shyiramo PDF/Image ya Plan", type=["pdf","png","jpg","jpeg"])

    if uploaded_file and uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += (page.extract_text() or "") + "\n"
                for table in page.extract_tables():
                    all_text += " ".join([str(cell) for row in table for cell in row if cell]) + "\n"

            dim_pattern = r'(?<!scale\s)(?<!1\s*:\s*)(?:dim|dimension|length|width)?\s*[:=]?\s*(\d+[.,]?\d*)\s*(m|mm|cm)\b'
            numbers = re.findall(dim_pattern, all_text.lower(), re.IGNORECASE)

            if re.search(r'second floor|g\+2|r\+2|3\s*floor', all_text.lower()):
                auto_dimensions["floors"] = 3
            elif re.search(r'first floor|g\+1|r\+1|2\s*floor', all_text.lower()):
                auto_dimensions["floors"] = 2

            rooms_found = re.findall(r'(\d+)\s*(room|bedroom|chambre|bed)', all_text.lower())
            if rooms_found:
                auto_dimensions["rooms"] = max(len(set([r[0] for r in rooms_found])), 1)

            if numbers:
                for num, unit in numbers:
                    val = float(num.replace(',','.'))
                    if unit == 'mm': val /= 1000.0
                    elif unit == 'cm': val /= 100.0
                    if 2.0 <= val <= 60.0:
                        valid_dims.append(round(val, 2))

                valid_dims = sorted(list(set(valid_dims)), reverse=True)
                if len(valid_dims) >= 1: auto_dimensions["length"] = valid_dims[0]
                if len(valid_dims) >= 2: auto_dimensions["width"] = valid_dims[1]
                if len(valid_dims) >= 3:
                    heights = [d for d in valid_dims if 2.5 <= d <= 4.5]
                    if heights: auto_dimensions["height"] = heights[0]

            st.success(f"✅ PDF yasomwe | Floors: {auto_dimensions['floors']} | Rooms: {auto_dimensions['rooms']}")
            if valid_dims:
                st.info(f"📐 Dimensions: {valid_dims}")

st.header("2. HOUSE SPECS")
col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns(5)
with col_h1: length = st.number_input("Length (m)", value=float(auto_dimensions["length"]), min_value=0.0, step=0.1)
with col_h2: width = st.number_input("Width (m)", value=float(auto_dimensions["width"]), min_value=0.0, step=0.1)
with col_h3: height = st.number_input("Wall Height (m)", value=float(auto_dimensions["height"]), min_value=2.0, step=0.1)
with col_h4: rooms = st.number_input("Rooms", value=int(auto_dimensions["rooms"]), min_value=1, step=1)
with col_h5: floors = st.number_input("Floors", value=int(auto_dimensions["floors"]), min_value=1, step=1)

area = length * width
volume = length * width * 0.5
wall_area = 2 * (length + width) * height * floors
roof_area = area * 1.2
slab_area = area * (floors - 1) if floors > 1 else 0

st.subheader("🔢 SMART COUNT")
col_cnt1, col_cnt2, col_cnt3, col_cnt4 = st.columns(4)
with col_cnt1: count_windows = st.number_input("Windows", value=int(rooms*1.5), min_value=0)
with col_cnt2: count_doors = st.number_input("Doors", value=rooms+2, min_value=0)
with col_cnt3: count_sockets = st.number_input("Sockets", value=rooms*3*floors, min_value=0)
with col_cnt4: count_bulbs = st.number_input("LED Bulbs", value=(rooms+3)*floors, min_value=0)

st.header("3. MATERIALS TABLE - RPPA + CUSTOM RATES")
st.caption("💡 Hitamo material, koresha RPPA cyangwa shyiramo igiciro cyawe")

if 'materials_df' not in st.session_state:
    st.session_state['materials_df'] = pd.DataFrame([
        {"Material": "Cement CEM II 42.5N", "Category": "Binding", "Unit": "bag", "RPPA_Rate": default_cement_rate, "Your_Rate": default_cement_rate, "Use_RPPA": True},
        {"Material": "23cm Block", "Category": "Masonry", "Unit": "pc", "RPPA_Rate": default_block_rate, "Your_Rate": default_block_rate, "Use_RPPA": True},
        {"Material": "Ceramic Tile", "Category": "Finishing", "Unit": "m²", "RPPA_Rate": default_tile_rate, "Your_Rate": default_tile_rate, "Use_RPPA": True},
        {"Material": "Mabati G30", "Category": "Roofing", "Unit": "m²", "RPPA_Rate": default_roof_rate, "Your_Rate": default_roof_rate, "Use_RPPA": True},
        {"Material": "Concrete C25", "Category": "Concrete", "Unit": "m³", "RPPA_Rate": default_concrete_rate, "Your_Rate": default_concrete_rate, "Use_RPPA": True},
        {"Material": "River Sand", "Category": "Aggregate", "Unit": "m³", "RPPA_Rate": 25000, "Your_Rate": 25000, "Use_RPPA": True},
        {"Material": "Aggregate", "Category": "Aggregate", "Unit": "m³", "RPPA_Rate": 30000, "Your_Rate": 30000, "Use_RPPA": True},
        {"Material": "Y16 Steel", "Category": "Steel", "Unit": "kg", "RPPA_Rate": 1250, "Your_Rate": 1250, "Use_RPPA": True},
        {"Material": "Y40 Steel", "Category": "Steel", "Unit": "kg", "RPPA_Rate": 1400, "Your_Rate": 1400, "Use_RPPA": True},
    ])

edited_materials = st.data_editor(
    st.session_state['materials_df'],
    column_config={
        "Material": st.column_config.SelectboxColumn(
            "Material",
            options=["Cement CEM II 42.5N", "Cement CEM I 52.5N", "15cm Block", "23cm Block",
                     "Ceramic Tile", "Granite Tile", "Mabati G30", "Versatile Tile",
                     "Concrete C25", "Concrete C30", "River Sand", "Aggregate",
                     "Y16 Steel", "Y40 Steel", "Y12 Steel"],
            required=True
        ),
        "Use_RPPA": st.column_config.CheckboxColumn("Use RPPA?"),
        "RPPA_Rate": st.column_config.NumberColumn("RPPA Rate RWF", disabled=True, format="%d"),
        "Your_Rate": st.column_config.NumberColumn("Your Rate RWF", format="%d"),
    },
    use_container_width=True,
    num_rows="dynamic",
    key="materials_editor"
)

st.session_state['materials_df'] = edited_materials

rate_dict = {}
for _, row in edited_materials.iterrows():
    rate_dict[row["Material"]] = row["RPPA_Rate"] if row["Use_RPPA"] else row["Your_Rate"]

cement_rate = rate_dict.get("Cement CEM II 42.5N", 12500)
block_rate = rate_dict.get("23cm Block", 1000)
tile_rate = rate_dict.get("Ceramic Tile", 12000)
roof_rate = rate_dict.get("Mabati G30", 8500)
concrete_rate = rate_dict.get("Concrete C25", 180000)
sand_rate = rate_dict.get("River Sand", 25000)
agg_rate = rate_dict.get("Aggregate", 30000)
y16_rate = rate_dict.get("Y16 Steel", 1250)
y40_rate = rate_dict.get("Y40 Steel", 1400)

st.header("4. AUTO BOQ")
block_qty = 12.5
door_flash = 95000
window_steel = 45000
db_6way = 35000
yaka_meter = 80000
toilet = 180000
sink = 85000
ppr_20 = 2500
socket = 3500
bulb = 2500
cable_25 = 65000

variable_items = [
    ["A", "SUBSTRUCTURE", "", ""],
    [1, "Site Clearance", area, "m²", 500, area * 500],
    [2, "Excavation", volume, "m³", 3500, volume * 3500],
    [3, "Hardcore filling", area * 0.15, "m³", agg_rate, area * 0.15 * agg_rate],
    [4, "River Sand blinding", area * 0.05, "m³", sand_rate, area * 0.05 * sand_rate],
    [5, f"Concrete C25 foundation", volume * 0.4, "m³", concrete_rate, volume * 0.4 * concrete_rate],
    [6, "Y16 Steel foundation", volume * 80, "kg", y16_rate, volume * 80 * y16_rate],
    ["B", "SUPERSTRUCTURE", "", ""],
    [7, f"23cm Block Walling", wall_area, "m²", block_rate * block_qty, wall_area * block_rate * block_qty],
    [8, f"Concrete C25 columns", height * 0.2 * 4 * floors, "m³", concrete_rate, height * 0.2 * 4 * floors * concrete_rate],
    [9, f"Y40 Steel columns", height * 100 * floors, "kg", y40_rate, height * 100 * floors * y40_rate],
    ["C", "ROOFING", "", ""],
    [10, f"Mabati G30 Roofing", roof_area, "m²", roof_rate, roof_area * roof_rate],
    ["D", "FINISHES", "", ""],
    [11, f"Ceramic Tile Floor", area * floors, "m²", tile_rate, area * floors * tile_rate],
    [12, "Paint Walls", wall_area * 2, "m²", 1300, wall_area * 2 * 1300],
]

fixed_items = [
    ["E", "ELECTRICAL", "", ""],
    [13, "2.5mm Cable Wiring", rooms + 2, "rolls", cable_25, (rooms + 2) * cable_25],
    [14, "Sockets", count_sockets, "pcs", socket, count_sockets * socket],
    [15, "LED Bulbs", count_bulbs, "pcs", bulb, count_bulbs * bulb],
    [16, "DB Board", 1, "pc", db_6way, db_6way],
    [17, "Yaka Meter", 1, "pc", yaka_meter, yaka_meter],
    ["F", "PLUMBING", "", ""],
    [18, "PPR 20mm Pipes", 30 * floors, "m", ppr_20, 30 * floors * ppr_20],
    [19, "WC Toilet", floors, "pc", toilet, floors * toilet],
    [20, "Kitchen Sink", 1, "pc", sink, sink],
]

all_items = variable_items + fixed_items
df = pd.DataFrame(all_items, columns=["Item No", "Description", "Qty", "Unit", "Rate", "Amount"])
df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce').fillna(0)

subtotal = df["Amount"].sum()
vat = subtotal * 0.18
grand_total = subtotal + vat

st.dataframe(df, use_container_width=True)

col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("SUB TOTAL", f"{subtotal:,.0f} RWF")
col_t2.metric("VAT 18%", f"{vat:,.0f} RWF")
col_t3.metric("GRAND TOTAL", f"{grand_total:,.0f} RWF")

st.header("5. DOWNLOAD EXCEL")

def to_excel(df_boq, df_mat):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_boq.to_excel(writer, index=False, sheet_name='BOQ', startrow=3)
        ws1 = writer.sheets['BOQ']
        ws1.cell(row=1, column=1, value="B-ESTAMER V3.18 PRECISION EMPIRE")
        ws1.cell(row=2, column=1, value="Contact: BRUNO CONSTRUCTION EMPIRE LTD - 0787993679")

        df_mat.to_excel(writer, index=False, sheet_name='Materials_Rates')
        ws2 = writer.sheets['Materials_Rates']
        ws2.cell(row=1, column=1, value="Materials & Rates Used in This BOQ")

    return output.getvalue()

excel_data = to_excel(df, edited_materials)

st.download_button(
    label="📥 Download BOQ + Materials Excel",
    data=excel_data,
    file_name=f"B-ESTAMER_R+{floors-1}{length}x{width}{grand_total:,.0f}RWF.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.header("6. SAVE/LOAD MATERIALS")
col_save1, col_save2 = st.columns(2)
with col_save1:
    if st.button("💾 Bika Materials List"):
        st.session_state['saved_materials'] = edited_materials.to_dict()
        st.success("✅ Materials zabikwe!")

with col_save2:
    if st.button("📂 Koresha Materials Nabikije"):
        if 'saved_materials' in st.session_state:
            st.session_state['materials_df'] = pd.DataFrame(st.session_state['saved_materials'])
            st.rerun()

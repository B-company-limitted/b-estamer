# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V4.7 ULTIMATE - Y50 STEEL + MIX CALC + BAR CUTTING + ALL MATERIALS | 0787993679

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import math

st.set_page_config(page_title="B-ESTAMER 4.7", layout="wide")
st.title("B-ESTAMER 4.7 ULTIMATE 🏗️")
st.caption("Y50 Steel + Mix Ratio + Bar Cutting + Brick Calc + 35+ Materials + 999M Qty")

# ============= MIX RATIO DATABASE =============
MIX_RATIOS = {
    "C15 1:3:6": {"Cement":1, "Sand":3, "Stone":6, "Water":0.5},
    "C20 1:2:4": {"Cement":1, "Sand":2, "Stone":4, "Water":0.5},
    "C25 1:2:3": {"Cement":1, "Sand":2, "Stone":3, "Water":0.5},
    "C30 1:1.5:3": {"Cement":1, "Sand":1.5, "Stone":3, "Water":0.45},
    "C35 1:1:2": {"Cement":1, "Sand":1, "Stone":2, "Water":0.4},
    "C40 1:1:1.5": {"Cement":1, "Sand":1, "Stone":1.5, "Water":0.35},
    "Mortar 1:3": {"Cement":1, "Sand":3},
    "Mortar 1:4": {"Cement":1, "Sand":4},
    "Mortar 1:5": {"Cement":1, "Sand":5},
    "Mortar 1:6": {"Cement":1, "Sand":6},
    "Screed 1:4": {"Cement":1, "Sand":4},
}

# ============= MATERIAL TREE - MAIN + SUB TYPES =============
MATERIAL_TREE = {
    "CEMENT": ["CEM II 42.5N","CEM I 52.5N","White Cement","Quick Set Cement","Portland Cement"],
    "SAND": ["River Sand","Crushed Sand","Plaster Sand","Filling Sand","Quarry Dust"],
    "STONE": ["Stone 20mm","Stone 40mm","Ballast","Hardcore","Aggregate Dust","Chippings"],
    "BRICK": ["Clay Brick 6 inch","Clay Brick 4 inch","Concrete Block 23cm Solid","Concrete Block 15cm Solid","Concrete Block 23cm Hollow","Concrete Block 15cm Hollow","Paving Block","Face Brick"],
    "STEEL_BAR": ["R6 Stirrups","R8 Stirrups","R10 Steel","Y12 Steel","Y16 Steel","Y20 Steel","Y25 Steel","Y32 Steel","Y40 Steel","Y50 Steel"],
    "TIMBER": ["Cypress 2x2","Cypress 3x2","Cypress 4x2","Plywood 18mm","Marine Board 18mm","MDF Board","Hardwood","Softwood","Pine"],
    "IRON_SHEET": ["Mabati G30 Versatile","Mabati G28 IT4","Mabati G30 Corrugated","Resincot","Gauge 28","Gauge 30","Aluminium Sheet"],
    "PAINT": ["Emulsion Paint","Weather Guard","Undercoat","Varnish","Oil Based","Water Based","Primer"],
    "TILES": ["Ceramic Tile 30x30","Ceramic Tile 60x60","Porcelain Tile","Granite Tile","Marble Tile","PVC Tile","Terrazzo"],
    "CONCRETE": ["Concrete C15","Concrete C20","Concrete C25","Concrete C30","Concrete C35","Concrete C40","Ready Mix C25","Ready Mix C30"],
    "GLASS": ["Glass 4mm Clear","Glass 5mm Tinted","Glass 6mm Laminated","Mirror","Frosted Glass","Bullet Proof"],
    "PIPES": ["PPR 20mm","PPR 25mm","PPR 32mm","PPR 40mm","PVC 4inch Waste","PVC 2inch Waste","PVC 6inch","HDPE 50mm","GI Pipe 1inch"],
    "WIRES": ["Cable 1.5mm","Cable 2.5mm","Cable 4mm","Cable 6mm","Cable 10mm","Cable 16mm","Twin Earth","Armoured Cable"],
    "DOORS": ["Steel Door 90x210","Flush Door","Panel Door","PVC Door","Glass Door","Security Door"],
    "WINDOWS": ["Aluminium Sliding","Aluminium Casement","Louver Window","Wooden Window","UPVC Window"],
    "WATERPROOF": ["APP Membrane","Bitumen Paint","Cementitious Waterproof","Liquid Membrane","EPDM"],
    "CEILING": ["Gypsum Board","PVC Ceiling","Acoustic Ceiling","Wooden T&G","Suspended Ceiling","Mineral Fiber"],
    "NAILS": ["Nails 1 inch","Nails 2 inch","Nails 3 inch","Nails 4 inch","Roofing Nails","Concrete Nails","U-Nails"],
    "BINDING": ["Binding Wire","BRC Mesh A142","BRC Mesh A98","Chain Link","Barbed Wire"],
}

# ============= FULL MATERIALS DATABASE WITH DETAILS =============
if 'materials' not in st.session_state:
    st.session_state['materials'] = pd.DataFrame([
        # CEMENT
        {"Section":"CEMENT","Item":"CEM II 42.5N","Unit":"bag","Rate":12500,"Weight":50},
        {"Section":"CEMENT","Item":"CEM I 52.5N","Unit":"bag","Rate":14500,"Weight":50},
        {"Section":"CEMENT","Item":"White Cement","Unit":"bag","Rate":25000,"Weight":50},
        {"Section":"CEMENT","Item":"Quick Set Cement","Unit":"bag","Rate":16000,"Weight":50},
        {"Section":"CEMENT","Item":"Portland Cement","Unit":"bag","Rate":13000,"Weight":50},

        # SAND
        {"Section":"SAND","Item":"River Sand","Unit":"m3","Rate":25000,"Density":1600},
        {"Section":"SAND","Item":"Crushed Sand","Unit":"m3","Rate":22000,"Density":1550},
        {"Section":"SAND","Item":"Plaster Sand","Unit":"m3","Rate":28000,"Density":1600},
        {"Section":"SAND","Item":"Filling Sand","Unit":"m3","Rate":18000,"Density":1500},
        {"Section":"SAND","Item":"Quarry Dust","Unit":"m3","Rate":18000,"Density":1450},

        # STONE
        {"Section":"STONE","Item":"Stone 20mm","Unit":"m3","Rate":32000,"Density":1450},
        {"Section":"STONE","Item":"Stone 40mm","Unit":"m3","Rate":30000,"Density":1400},
        {"Section":"STONE","Item":"Ballast","Unit":"m3","Rate":28000,"Density":1500},
        {"Section":"STONE","Item":"Hardcore","Unit":"m3","Rate":20000,"Density":1600},
        {"Section":"STONE","Item":"Aggregate Dust","Unit":"m3","Rate":17000,"Density":1400},
        {"Section":"STONE","Item":"Chippings","Unit":"m3","Rate":35000,"Density":1400},

        # BRICK
        {"Section":"BRICK","Item":"Clay Brick 6 inch","Unit":"pc","Rate":250},
        {"Section":"BRICK","Item":"Clay Brick 4 inch","Unit":"pc","Rate":180},
        {"Section":"BRICK","Item":"Concrete Block 23cm Solid","Unit":"pc","Rate":1000},
        {"Section":"BRICK","Item":"Concrete Block 15cm Solid","Unit":"pc","Rate":800},
        {"Section":"BRICK","Item":"Concrete Block 23cm Hollow","Unit":"pc","Rate":850},
        {"Section":"BRICK","Item":"Concrete Block 15cm Hollow","Unit":"pc","Rate":700},
        {"Section":"BRICK","Item":"Paving Block","Unit":"pc","Rate":300},
        {"Section":"BRICK","Item":"Face Brick","Unit":"pc","Rate":450},

        # STEEL_BAR - Y50 INCLUDED
        {"Section":"STEEL_BAR","Item":"R6 Stirrups","Unit":"kg","Rate":1350,"Dia":6,"Weight_per_m":0.222,"Length":12},
        {"Section":"STEEL_BAR","Item":"R8 Stirrups","Unit":"kg","Rate":1320,"Dia":8,"Weight_per_m":0.395,"Length":12},
        {"Section":"STEEL_BAR","Item":"R10 Steel","Unit":"kg","Rate":1300,"Dia":10,"Weight_per_m":0.617,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y12 Steel","Unit":"kg","Rate":1300,"Dia":12,"Weight_per_m":0.888,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y16 Steel","Unit":"kg","Rate":1250,"Dia":16,"Weight_per_m":1.578,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y20 Steel","Unit":"kg","Rate":1260,"Dia":20,"Weight_per_m":2.466,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y25 Steel","Unit":"kg","Rate":1270,"Dia":25,"Weight_per_m":3.853,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y32 Steel","Unit":"kg","Rate":1280,"Dia":32,"Weight_per_m":6.313,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y40 Steel","Unit":"kg","Rate":1400,"Dia":40,"Weight_per_m":9.865,"Length":12},
        {"Section":"STEEL_BAR","Item":"Y50 Steel","Unit":"kg","Rate":1550,"Dia":50,"Weight_per_m":15.413,"Length":12},

        # BINDING
        {"Section":"BINDING","Item":"Binding Wire","Unit":"kg","Rate":2000},
        {"Section":"BINDING","Item":"BRC Mesh A142","Unit":"roll","Rate":85000,"Area":50},
        {"Section":"BINDING","Item":"BRC Mesh A98","Unit":"roll","Rate":65000,"Area":50},
        {"Section":"BINDING","Item":"Chain Link","Unit":"m2","Rate":3500},
        {"Section":"BINDING","Item":"Barbed Wire","Unit":"roll","Rate":25000},

        # TIMBER
        {"Section":"TIMBER","Item":"Cypress 2x2","Unit":"m","Rate":450},
        {"Section":"TIMBER","Item":"Cypress 3x2","Unit":"m","Rate":650},
        {"Section":"TIMBER","Item":"Cypress 4x2","Unit":"m","Rate":850},
        {"Section":"TIMBER","Item":"Plywood 18mm","Unit":"pc","Rate":55000},
        {"Section":"TIMBER","Item":"Marine Board 18mm","Unit":"pc","Rate":85000},
        {"Section":"TIMBER","Item":"MDF Board","Unit":"pc","Rate":45000},
        {"Section":"TIMBER","Item":"Hardwood","Unit":"m3","Rate":450000},
        {"Section":"TIMBER","Item":"Softwood","Unit":"m3","Rate":280000},
        {"Section":"TIMBER","Item":"Pine","Unit":"m3","Rate":320000},

        # IRON_SHEET
        {"Section":"IRON_SHEET","Item":"Mabati G30 Versatile","Unit":"m2","Rate":8500},
        {"Section":"IRON_SHEET","Item":"Mabati G28 IT4","Unit":"m2","Rate":9500},
        {"Section":"IRON_SHEET","Item":"Mabati G30 Corrugated","Unit":"m2","Rate":7500},
        {"Section":"IRON_SHEET","Item":"Resincot","Unit":"m2","Rate":10500},
        {"Section":"IRON_SHEET","Item":"Gauge 28","Unit":"m2","Rate":9800},
        {"Section":"IRON_SHEET","Item":"Gauge 30","Unit":"m2","Rate":8200},
        {"Section":"IRON_SHEET","Item":"Aluminium Sheet","Unit":"m2","Rate":15000},

        # PAINT
        {"Section":"PAINT","Item":"Emulsion Paint","Unit":"L","Rate":8500},
        {"Section":"PAINT","Item":"Weather Guard","Unit":"L","Rate":12000},
        {"Section":"PAINT","Item":"Undercoat","Unit":"L","Rate":7500},
        {"Section":"PAINT","Item":"Varnish","Unit":"L","Rate":15000},
        {"Section":"PAINT","Item":"Oil Based","Unit":"L","Rate":11000},
        {"Section":"PAINT","Item":"Water Based","Unit":"L","Rate":9000},
        {"Section":"PAINT","Item":"Primer","Unit":"L","Rate":8000},

        # TILES
        {"Section":"TILES","Item":"Ceramic Tile 30x30","Unit":"m2","Rate":12000},
        {"Section":"TILES","Item":"Ceramic Tile 60x60","Unit":"m2","Rate":18000},
        {"Section":"TILES","Item":"Porcelain Tile","Unit":"m2","Rate":25000},
        {"Section":"TILES","Item":"Granite Tile","Unit":"m2","Rate":45000},
        {"Section":"TILES","Item":"Marble Tile","Unit":"m2","Rate":65000},
        {"Section":"TILES","Item":"PVC Tile","Unit":"m2","Rate":8000},
        {"Section":"TILES","Item":"Terrazzo","Unit":"m2","Rate":35000},

        # CONCRETE
        {"Section":"CONCRETE","Item":"Concrete C15","Unit":"m3","Rate":160000},
        {"Section":"CONCRETE","Item":"Concrete C20","Unit":"m3","Rate":170000},
        {"Section":"CONCRETE","Item":"Concrete C25","Unit":"m3","Rate":180000},
        {"Section":"CONCRETE","Item":"Concrete C30","Unit":"m3","Rate":210000},
        {"Section":"CONCRETE","Item":"Concrete C35","Unit":"m3","Rate":240000},
        {"Section":"CONCRETE","Item":"Concrete C40","Unit":"m3","Rate":280000},
        {"Section":"CONCRETE","Item":"Ready Mix C25","Unit":"m3","Rate":195000},
        {"Section":"CONCRETE","Item":"Ready Mix C30","Unit":"m3","Rate":225000},

        # GLASS
        {"Section":"GLASS","Item":"Glass 4mm Clear","Unit":"m2","Rate":12000},
        {"Section":"GLASS","Item":"Glass 5mm Tinted","Unit":"m2","Rate":18000},
        {"Section":"GLASS","Item":"Glass 6mm Laminated","Unit":"m2","Rate":28000},
        {"Section":"GLASS","Item":"Mirror","Unit":"m2","Rate":25000},
        {"Section":"GLASS","Item":"Frosted Glass","Unit":"m2","Rate":22000},
        {"Section":"GLASS","Item":"Bullet Proof","Unit":"m2","Rate":180000},

        # PIPES
        {"Section":"PIPES","Item":"PPR 20mm","Unit":"m","Rate":2500},
        {"Section":"PIPES","Item":"PPR 25mm","Unit":"m","Rate":3500},
        {"Section":"PIPES","Item":"PPR 32mm","Unit":"m","Rate":5500},
        {"Section":"PIPES","Item":"PPR 40mm","Unit":"m","Rate":8500},
        {"Section":"PIPES","Item":"PVC 4inch Waste","Unit":"m","Rate":4500},
        {"Section":"PIPES","Item":"PVC 2inch Waste","Unit":"m","Rate":2800},
        {"Section":"PIPES","Item":"PVC 6inch","Unit":"m","Rate":8500},
        {"Section":"PIPES","Item":"HDPE 50mm","Unit":"m","Rate":6500},
        {"Section":"PIPES","Item":"GI Pipe 1inch","Unit":"m","Rate":4500},

        # WIRES
        {"Section":"WIRES","Item":"Cable 1.5mm","Unit":"m","Rate":900},
        {"Section":"WIRES","Item":"Cable 2.5mm","Unit":"m","Rate":1200},
        {"Section":"WIRES","Item":"Cable 4mm","Unit":"m","Rate":2200},
        {"Section":"WIRES","Item":"Cable 6mm","Unit":"m","Rate":3500},
        {"Section":"WIRES","Item":"Cable 10mm","Unit":"m","Rate":6500},
        {"Section":"WIRES","Item":"Cable 16mm","Unit":"m","Rate":12000},
        {"Section":"WIRES","Item":"Twin Earth","Unit":"m","Rate":2800},
        {"Section":"WIRES","Item":"Armoured Cable","Unit":"m","Rate":15000},

        # DOORS
        {"Section":"DOORS","Item":"Steel Door 90x210","Unit":"pc","Rate":95000},
        {"Section":"DOORS","Item":"Flush Door","Unit":"pc","Rate":45000},
        {"Section":"DOORS","Item":"Panel Door","Unit":"pc","Rate":75000},
        {"Section":"DOORS","Item":"PVC Door","Unit":"pc","Rate":65000},
        {"Section":"DOORS","Item":"Glass Door","Unit":"pc","Rate":120000},
        {"Section":"DOORS","Item":"Security Door","Unit":"pc","Rate":180000},

        # WINDOWS
        {"Section":"WINDOWS","Item":"Aluminium Sliding","Unit":"m2","Rate":65000},
        {"Section":"WINDOWS","Item":"Aluminium Casement","Unit":"m2","Rate":70000},
        {"Section":"WINDOWS","Item":"Louver Window","Unit":"m2","Rate":45000},
        {"Section":"WINDOWS","Item":"Wooden Window","Unit":"m2","Rate":55000},
        {"Section":"WINDOWS","Item":"UPVC Window","Unit":"m2","Rate":85000},

        # WATERPROOF
        {"Section":"WATERPROOF","Item":"APP Membrane","Unit":"roll","Rate":95000},
        {"Section":"WATERPROOF","Item":"Bitumen Paint","Unit":"L","Rate":6500},
        {"Section":"WATERPROOF","Item":"Cementitious Waterproof","Unit":"bag","Rate":35000},
        {"Section":"WATERPROOF","Item":"Liquid Membrane","Unit":"L","Rate":12000},
        {"Section":"WATERPROOF","Item":"EPDM","Unit":"m2","Rate":18000},

        # CEILING
        {"Section":"CEILING","Item":"Gypsum Board","Unit":"pc","Rate":18000},
        {"Section":"CEILING","Item":"PVC Ceiling","Unit":"m2","Rate":12000},
        {"Section":"CEILING","Item":"Acoustic Ceiling","Unit":"m2","Rate":25000},
        {"Section":"CEILING","Item":"Wooden T&G","Unit":"m2","Rate":18000},
        {"Section":"CEILING","Item":"Suspended Ceiling","Unit":"m2","Rate":22000},
        {"Section":"CEILING","Item":"Mineral Fiber","Unit":"m2","Rate":20000},

        # NAILS
        {"Section":"NAILS","Item":"Nails 1 inch","Unit":"kg","Rate":1800},
        {"Section":"NAILS","Item":"Nails 2 inch","Unit":"kg","Rate":1800},
        {"Section":"NAILS","Item":"Nails 3 inch","Unit":"kg","Rate":1800},
        {"Section":"NAILS","Item":"Nails 4 inch","Unit":"kg","Rate":1800},
        {"Section":"NAILS","Item":"Roofing Nails","Unit":"kg","Rate":2500},
        {"Section":"NAILS","Item":"Concrete Nails","Unit":"kg","Rate":2200},
        {"Section":"NAILS","Item":"U-Nails","Unit":"kg","Rate":2000},
    ])

# ============= SESSION STATE =============
if 'selected_main' not in st.session_state:
    st.session_state['selected_main'] = "CEMENT"
if 'selected_sub' not in st.session_state:
    st.session_state['selected_sub'] = None
if 'measurements' not in st.session_state:
    st.session_state['measurements'] = []

tabs = st.tabs(["1. Mix Calculator", "2. Bar Cutting", "3. Brick Wall", "4. Material Browser", "5. All Materials", "6. BOQ"])

# ===== TAB 1: MIX RATIO CALCULATOR =====
with tabs[0]:
    st.header("Mix Ratio Calculator - Y50 Support + High Capacity")

    col1, col2, col3 = st.columns(3)
    with col1:
        mix = st.selectbox("Select Mix Ratio", list(MIX_RATIOS.keys()), key="mix_sel")
    with col2:
        volume = st.number_input("Volume m3", 10.0, step=1.0, min_value=0.1, max_value=999999999.0, key="mix_vol")
    with col3:
        waste = st.number_input("Waste Percent", 5.0, step=1.0, min_value=0.0, key="mix_waste")

    if st.button("Calculate Materials", type="primary", key="mix_calc"):
        ratio = MIX_RATIOS[mix]
        total_parts = sum([v for k,v in ratio.items() if k!="Water"])

        st.subheader(f"Materials for {volume:,.1f} m3 of {mix}")
        results = []

        if "Cement" in ratio:
            cement_bags = (volume * ratio["Cement"] / total_parts * 2400) / 50
            cement_bags = cement_bags * (1 + waste/100)
            results.append(["Cement CEM II 42.5N", round(cement_bags,1), "bags"])

        if "Sand" in ratio:
            sand_m3 = volume * ratio["Sand"] / total_parts * (1 + waste/100)
            results.append(["River Sand", round(sand_m3,2), "m3"])

        if "Stone" in ratio:
            stone_m3 = volume * ratio["Stone"] / total_parts * (1 + waste/100)
            results.append(["Stone 20mm", round(stone_m3,2), "m3"])

        if "Water" in ratio:
            water_liters = volume * ratio["Water"] * 1000
            results.append(["Water", round(water_liters,0), "liters"])

        st.dataframe(pd.DataFrame(results, columns=["Material","Qty","Unit"]), use_container_width=True, hide_index=True)

        if st.button("Add to BOQ", key="mix_add"):
            for r in results:
                if r[0]!="Water":
                    st.session_state['measurements'].append({
                        "Section":"Concrete", "Item":r[0], "Qty":r[1], "Unit":r[2], "Source":"Mix Ratio"
                    })
            st.success("Added to BOQ!")

# ===== TAB 2: BAR CUTTING LIST - Y50 INCLUDED =====
with tabs[1]:
    st.header("Bar Cutting List - Y6 to Y50 Steel")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        steel_list = st.session_state['materials'][st.session_state['materials']['Section']=='STEEL_BAR']['Item'].tolist()
        steel_type = st.selectbox("Steel Bar Type", steel_list, key="bar_type")
    with col2:
        cutting_length = st.number_input("Cutting Length m", 3.0, step=0.1, min_value=0.1, max_value=12.0, key="bar_cut")
    with col3:
        num_bars = st.number_input("Number of Bars", 10, step=1, min_value=1, max_value=999999, key="bar_num")
    with col4:
        lap_length = st.number_input("Lap Length m", 0.4, step=0.1, min_value=0.0, key="bar_lap")

    if st.button("Generate Cutting List", type="primary", key="bar_gen"):
        mat = st.session_state['materials'][st.session_state['materials']['Item']==steel_type].iloc[0]
        bar_length = 12.0
        weight_per_m = mat['Weight_per_m']

        total_length_needed = (cutting_length + lap_length) * num_bars
        bars_12m_needed = math.ceil(total_length_needed / bar_length)
        total_weight = total_length_needed * weight_per_m
        waste_percent = ((bars_12m_needed * bar_length - total_length_needed) / total_length_needed) * 100
        binding_wire = (total_weight / 1000) * 15

        st.subheader(f"Cutting List for {steel_type}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Length", f"{total_length_needed:,.1f} m")
        col2.metric("12m Bars to Buy", f"{bars_12m_needed:,} pcs")
        col3.metric("Total Weight", f"{total_weight:,.1f} kg")
        col4.metric("Binding Wire", f"{binding_wire:.1f} kg")

        st.info(f"Diameter: {mat['Dia']}mm | Weight/m: {weight_per_m} kg | Waste: {waste_percent:.1f}% | Each bar cuts {math.floor(bar_length/cutting_length)} pieces")

        cutting_df = pd.DataFrame({
            "Bar Number": [f"Bar {i+1}" for i in range(min(bars_12m_needed,20))],
            "Full Length m": [bar_length]*min(bars_12m_needed,20),
            "Cuts per Bar": [math.floor(bar_length/cutting_length)]*min(bars_12m_needed,20),
            "Waste per Bar m": [round(bar_length % cutting_length,2)]*min(bars_12m_needed,20)
        })
        st.dataframe(cutting_df, use_container_width=True, hide_index=True)
        if bars_12m_needed > 20:
            st.caption(f"Showing first 20 bars. Total: {bars_12m_needed} bars")

        if st.button("Add Steel to BOQ", key="bar_add_boq"):
            st.session_state['measurements'].extend([
                {"Section":"STEEL_BAR", "Item":steel_type, "Qty":round(total_weight,1), "Unit":"kg", "Source":"Bar Cutting"},
                {"Section":"BINDING", "Item":"Binding Wire", "Qty":round(binding_wire,1), "Unit":"kg", "Source":"Bar Cutting"}
            ])
            st.success("Steel added to BOQ!")

# ===== TAB 3: BRICK WALL CALCULATOR =====
with tabs[2]:
    st.header("Brick Wall Calculator")

    col1, col2, col3 = st.columns(3)
    with col1:
        wall_length = st.number_input("Wall Length m", 10.0, step=0.1, min_value=0.1, max_value=99999.0, key="wall_len")
    with col2:
        wall_height = st.number_input("Wall Height m", 3.0, step=0.1, min_value=0.1, max_value=999.0, key="wall_ht")
    with col3:
        brick_list = st.session_state['materials'][st.session_state['materials']['Section']=='BRICK']['Item'].tolist()
        brick_type = st.selectbox("Brick/Block Type", brick_list, key="wall_brick")

    col1, col2 = st.columns(2)
    with col1:
        mortar_ratio = st.selectbox("Mortar Mix", ["Mortar 1:4","Mortar 1:5","Mortar 1:6"], key="wall_mortar")
    with col2:
        mortar_thickness = st.number_input("Mortar Thickness mm", 10, step=1, min_value=5, max_value=20, key="wall_thick")

    if st.button("Calculate Wall Materials", type="primary", key="wall_calc"):
        wall_area = wall_length * wall_height

        if "6 inch" in brick_type: bricks_needed = wall_area * 60
        elif "4 inch" in brick_type: bricks_needed = wall_area * 40
        elif "23cm" in brick_type: bricks_needed = wall_area * 12.5
        else: bricks_needed = wall_area * 12.5

        waste = 0.08
        bricks_total = bricks_needed * (1 + waste)

        mortar_volume = wall_area * mortar_thickness / 1000
        mortar_parts = MIX_RATIOS[mortar_ratio]
        total_parts = sum(mortar_parts.values())
        cement_bags = (mortar_volume * mortar_parts["Cement"] / total_parts * 2400) / 50 * 1.05
        sand_m3 = mortar_volume * mortar_parts["Sand"] / total_parts * 1.05

        st.subheader(f"Materials for {wall_area:,.1f} m2 Wall")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Bricks/Blocks", f"{bricks_total:,.0f} pcs")
        col2.metric("Cement", f"{cement_bags:.1f} bags")
        col3.metric("Sand", f"{sand_m3:.2f} m3")
        col4.metric("Mortar Vol", f"{mortar_volume:.2f} m3")

        if st.button("Add Wall to BOQ", key="wall_add"):
            st.session_state['measurements'].extend([
                {"Section":"BRICK", "Item":brick_type, "Qty":round(bricks_total,0), "Unit":"pc", "Source":"Wall Calc"},
                {"Section":"CEMENT", "Item":"CEM II 42.5N", "Qty":round(cement_bags,1), "Unit":"bag", "Source":"Wall Calc"},
                {"Section":"SAND", "Item":"River Sand", "Qty":round(sand_m3,2), "Unit":"m3", "Source":"Wall Calc"}
            ])
            st.success("Wall materials added to BOQ!")

# ===== TAB 4: MATERIAL BROWSER =====
with tabs[3]:
    st.header("1. Kanda Material → Reba Sub-Types")

    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader("Main Materials")
        main_material = st.radio("Hitamo Material:", list(MATERIAL_TREE.keys()), key="main_radio_v2")
        st.session_state['selected_main'] = main_material

    with col2:
        st.subheader(f"Sub-Types za {st.session_state['selected_main']}")
        if st.session_state['selected_main']:
            sub_types = MATERIAL_TREE[st.session_state['selected_main']]

            cols = st.columns(3)
            for idx, sub in enumerate(sub_types):
                with cols[idx % 3]:
                    if st.button(sub, key=f"sub_{sub}_v2", use_container_width=True):
                        st.session_state['selected_sub'] = sub
                        st.rerun()

            if st.session_state['selected_sub']:
                st.success(f"✅ Wahisemo: *{st.session_state['selected_main']} → {st.session_state['selected_sub']}*")

                mat_data = st.session_state['materials'][
                    (st.session_state['materials']['Section']==st.session_state['selected_main']) &
                    (st.session_state['materials']['Item']==st.session_state['selected_sub'])
                ]

                if not mat_data.empty:
                    mat = mat_data.iloc[0]
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Unit", mat['Unit'])
                    col2.metric("Rate", f"{mat['Rate']:,} RWF")
                    if 'Dia' in mat: col3.metric("Diameter", f"{mat['Dia']}mm")
                    if 'Weight_per_m' in mat: col4.metric("Weight/m", f"{mat['Weight_per_m']} kg")

                    qty = st.number_input("Andika Quantity", 0.0, max_value=999999999.0, step=0.1, key="qty_input_v2")

                    if st.button("➕ Add to BOQ", type="primary", use_container_width=True, key="add_boq_v2"):
                        st.session_state['measurements'].append({
                            "Section": st.session_state['selected_main'],
                            "Item": st.session_state['selected_sub'],
                            "Qty": qty,
                            "Unit": mat['Unit'],
                            "Source": "Material Browser"
                        })
                        st.success(f"Added {qty} {mat['Unit']} of {st.session_state['selected_sub']} to BOQ!")
                        st.balloons()

# ===== TAB 5: ALL MATERIALS TABLE =====
with tabs[4]:
    st.header("Complete Materials Database - 35+ Items")
    section = st.selectbox("Filter Section", ["All"] + sorted(list(st.session_state['materials']['Section'].unique())), key="mat_filter")
    df_mat = st.session_state['materials']
    if section!= "All":
        df_mat = df_mat[df_mat['Section']==section]
    st.dataframe(df_mat, use_container_width=True, hide_index=True)
    st.success(f"Total: {len(st.session_state['materials'])} materials loaded | Max Qty: 999,999,999")

# ===== TAB 6: BOQ =====
with tabs[5]:
    st.header("Bill of Quantities - All Materials")
    if not st.session_state['measurements']:
        st.warning("Add materials from tabs above")
    else:
        df_meas = pd.DataFrame(st.session_state['measurements'])
        df_mat = st.session_state['materials']

        boq = []
        for _, row in df_meas.iterrows():
            mat = df_mat[df_mat['Item']==row['Item']].iloc[0]
            rate = mat['Rate']
            qty = row['Qty']

            if row['Section'] == "STEEL_BAR": waste = 0.03
            elif row['Section'] == "BRICK": waste = 0.08
            elif row['Section'] == "CONCRETE": waste = 0.05
            else: waste = 0.05

            gross_qty = qty * (1 + waste)
            amount = gross_qty * rate

            boq.append({
                "Section":row['Section'], "Item":row['Item'],
                "Source":row.get('Source','Manual'),
                "Net Qty":qty, "Waste %":round(waste*100,1),
                "Gross Qty":round(gross_qty,2), "Unit":row['Unit'],
                "Rate":rate, "Amount":round(amount,0)
            })

        df_boq = pd.DataFrame(boq)
        subtotal = df_boq['Amount'].sum()
        vat = subtotal * 0.18
        total = subtotal + vat

        st.dataframe(df_boq, use_container_width=True, hide_index=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Subtotal", f"{subtotal:,.0f} RWF")
        c2.metric("VAT 18%", f"{vat:,.0f} RWF")
        c3.metric("TOTAL", f"{total:,.0f} RWF")
        c4.metric("Items",

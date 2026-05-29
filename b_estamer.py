# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V4.3 FINAL - MIX RATIO + ALL STEEL + BRICK + STONE | 0787993679

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="B-ESTAMER 4.3", layout="wide")
st.title("B-ESTAMER 4.3 MIX RATIO CALCULATOR 🏗️")
st.caption("Brick + All Steel + Cement + Sand + Stone + Mix Ratios")

# ============= MIX RATIO DATABASE =============
MIX_RATIOS = {
    "C15 1:3:6": {"Cement":1, "Sand":3, "Stone":6, "Water":0.5},
    "C20 1:2:4": {"Cement":1, "Sand":2, "Stone":4, "Water":0.5},
    "C25 1:2:3": {"Cement":1, "Sand":2, "Stone":3, "Water":0.5},
    "C30 1:1.5:3": {"Cement":1, "Sand":1.5, "Stone":3, "Water":0.45},
    "C35 1:1:2": {"Cement":1, "Sand":1, "Stone":2, "Water":0.4},
    "Mortar 1:3": {"Cement":1, "Sand":3},
    "Mortar 1:4": {"Cement":1, "Sand":4},
    "Mortar 1:5": {"Cement":1, "Sand":5},
    "Mortar 1:6": {"Cement":1, "Sand":6},
}

# ============= FULL MATERIALS DATABASE =============
if 'materials' not in st.session_state:
    st.session_state['materials'] = pd.DataFrame([
        # ===== CEMENT =====
        {"Section":"Cement","Item":"Cement CEM II 42.5N","Unit":"bag","Rate":12500,"Weight":50},
        {"Section":"Cement","Item":"Cement CEM I 52.5N","Unit":"bag","Rate":14500,"Weight":50},

        # ===== SAND AND STONE =====
        {"Section":"Aggregates","Item":"River Sand","Unit":"m3","Rate":25000,"Density":1600},
        {"Section":"Aggregates","Item":"Stone 20mm","Unit":"m3","Rate":32000,"Density":1450},
        {"Section":"Aggregates","Item":"Stone 40mm","Unit":"m3","Rate":30000,"Density":1400},
        {"Section":"Aggregates","Item":"Quarry Dust","Unit":"m3","Rate":18000},

        # ===== BRICK SECTION =====
        {"Section":"Brick","Item":"Clay Brick 6 inch","Unit":"pc","Rate":250},
        {"Section":"Brick","Item":"Clay Brick 4 inch","Unit":"pc","Rate":180},
        {"Section":"Brick","Item":"Concrete Block 23cm","Unit":"pc","Rate":1000},
        {"Section":"Brick","Item":"Concrete Block 15cm","Unit":"pc","Rate":800},

        # ===== STEEL BARS ALL SIZES =====
        {"Section":"Steel","Item":"R6 Stirrups","Unit":"kg","Rate":1350,"Dia":6,"Weight_per_m":0.222},
        {"Section":"Steel","Item":"R8 Stirrups","Unit":"kg","Rate":1320,"Dia":8,"Weight_per_m":0.395},
        {"Section":"Steel","Item":"R10 Steel","Unit":"kg","Rate":1300,"Dia":10,"Weight_per_m":0.617},
        {"Section":"Steel","Item":"Y12 Steel","Unit":"kg","Rate":1300,"Dia":12,"Weight_per_m":0.888},
        {"Section":"Steel","Item":"Y16 Steel","Unit":"kg","Rate":1250,"Dia":16,"Weight_per_m":1.578},
        {"Section":"Steel","Item":"Y20 Steel","Unit":"kg","Rate":1260,"Dia":20,"Weight_per_m":2.466},
        {"Section":"Steel","Item":"Y25 Steel","Unit":"kg","Rate":1270,"Dia":25,"Weight_per_m":3.853},
        {"Section":"Steel","Item":"Y32 Steel","Unit":"kg","Rate":1280,"Dia":32,"Weight_per_m":6.313},
        {"Section":"Steel","Item":"Y40 Steel","Unit":"kg","Rate":1400,"Dia":40,"Weight_per_m":9.865},
        {"Section":"Steel","Item":"Binding Wire","Unit":"kg","Rate":2000},

        # ===== CONCRETE =====
        {"Section":"Concrete","Item":"Concrete C25","Unit":"m3","Rate":180000},
        {"Section":"Concrete","Item":"Concrete C30","Unit":"m3","Rate":210000},

        # ===== FINISHING =====
        {"Section":"Finishing","Item":"Plaster Sand","Unit":"m3","Rate":28000},
        {"Section":"Finishing","Item":"Ceramic Tile","Unit":"m2","Rate":12000},
        {"Section":"Finishing","Item":"Paint Emulsion","Unit":"m2","Rate":1300},
        {"Section":"Finishing","Item":"Mabati G30","Unit":"m2","Rate":8500},

        # ===== MEP =====
        {"Section":"MEP","Item":"PPR 20mm Pipe","Unit":"m","Rate":2500},
        {"Section":"MEP","Item":"2.5mm Cable","Unit":"m","Rate":1200},
        {"Section":"MEP","Item":"Socket Outlet","Unit":"pc","Rate":3500},

        # ===== DOORS AND WINDOWS =====
        {"Section":"Doors_Windows","Item":"Steel Door 90x210","Unit":"pc","Rate":95000},
        {"Section":"Doors_Windows","Item":"Aluminium Window","Unit":"m2","Rate":65000},
    ])

# ============= CONSTRAINTS =============
if 'constraints' not in st.session_state:
    st.session_state['constraints'] = {
        "Cement Bags per m3 C25": 6.5,
        "Sand m3 per m3 Concrete": 0.4,
        "Stone m3 per m3 Concrete": 0.8,
        "Bricks per m2 6inch Wall": 60,
        "Bricks per m2 4inch Wall": 40,
        "Blocks per m2 23cm": 12.5,
        "Concrete Waste Percent": 5,
        "Steel Waste Percent": 3,
        "Brick Waste Percent": 8,
    }

tabs = st.tabs(["Mix Ratio Calc", "Materials", "Constraints", "Takeoff", "BOQ"])

# ===== TAB 1: MIX RATIO CALCULATOR =====
with tabs[0]:
    st.header("Mix Ratio Calculator - Auto Bags per m3")

    col1, col2, col3 = st.columns(3)
    with col1:
        mix = st.selectbox("Select Mix Ratio", list(MIX_RATIOS.keys()))
    with col2:
        volume = st.number_input("Volume m3", 10.0, step=1.0)
    with col3:
        waste = st.number_input("Waste Percent", 5.0, step=1.0)

    if st.button("Calculate Materials", type="primary"):
        ratio = MIX_RATIOS[mix]
        total_parts = sum(ratio.values())

        st.subheader(f"Materials for {volume} m3 of {mix}")

        results = []
        if "Cement" in ratio:
            cement_bags = (volume * ratio["Cement"] / total_parts * 2400) / 50
            cement_bags = cement_bags * (1 + waste/100)
            results.append(["Cement", round(cement_bags,1), "bags"])

        if "Sand" in ratio:
            sand_m3 = volume * ratio["Sand"] / total_parts * (1 + waste/100)
            results.append(["River Sand", round(sand_m3,2), "m3"])

        if "Stone" in ratio:
            stone_m3 = volume * ratio["Stone"] / total_parts * (1 + waste/100)
            results.append(["Stone 20mm", round(stone_m3,2), "m3"])

        if "Water" in ratio:
            water_liters = volume * ratio["Water"] * 1000
            results.append(["Water", round(water_liters,0), "liters"])

        st.dataframe(pd.DataFrame(results, columns=["Material","Qty","Unit"]), use_container_width=True)

        if st.button("Add to Takeoff List"):
            for r in results:
                st.session_state.setdefault('measurements', []).append({
                    "Section":"Concrete", "Item":r[0], "Qty":r[1], "Unit":r[2]
                })
            st.success("Added to takeoff!")

# ===== TAB 2: MATERIALS TABLE =====
with tabs[1]:
    st.header("Complete Materials Database")

    section = st.selectbox("Filter Section", ["All"] + list(st.session_state['materials']['Section'].unique()))
    df_mat = st.session_state['materials']
    if section!= "All":
        df_mat = df_mat[df_mat['Section']==section]

    edited = st.data_editor(df_mat, use_container_width=True, num_rows="dynamic")
    st.session_state['materials'] = edited
    st.info(f"Total: {len(edited)} materials loaded")

# ===== TAB 3: CONSTRAINTS =====
with tabs[2]:
    st.header("Construction Constraints")
    cons_df = pd.DataFrame(list(st.session_state['constraints'].items()), columns=["Parameter","Value"])
    edited_cons = st.data_editor(cons_df, use_container_width=True, hide_index=True)
    st.session_state['constraints'] = dict(zip(edited_cons['Parameter'], edited_cons['Value']))

# ===== TAB 4: TAKEOFF =====
with tabs[3]:
    st.header("Manual Takeoff")

    if 'measurements' not in st.session_state:
        st.session_state['measurements'] = []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        section = st.selectbox("Section", st.session_state['materials']['Section'].unique())
    with col2:
        item = st.selectbox("Item", st.session_state['materials'][st.session_state['materials']['Section']==section]['Item'].tolist())
    with col3:
        qty = st.number_input("Quantity", 0.0, step=0.1)
    with col4:
        unit = st.session_state['materials'][st.session_state['materials']['Item']==item]['Unit'].iloc[0]
        st.text_input("Unit", unit, disabled=True)

    if st.button("Add Item"):
        st.session_state['measurements'].append({"Section":section, "Item":item, "Qty":qty, "Unit":unit})
        st.rerun()

    if st.session_state['measurements']:
        st.dataframe(pd.DataFrame(st.session_state['measurements']), use_container_width=True, hide_index=True)

# ===== TAB 5: BOQ =====
with tabs[4]:
    st.header("Bill of Quantities")

    if not st.session_state.get('measurements'):
        st.warning("Add measurements first")
    else:
        df_meas = pd.DataFrame(st.session_state['measurements'])
        df_mat = st.session_state['materials']
        cons = st.session_state['constraints']

        boq = []
        for _, row in df_meas.iterrows():
            mat = df_mat[df_mat['Item']==row['Item']].iloc[0]
            rate = mat['Rate']
            qty = row['Qty']

            if row['Section'] == "Steel": waste = cons['Steel Waste Percent']/100
            elif row['Section'] == "Brick": waste = cons['Brick Waste Percent']/100
            elif row['Section'] == "Concrete": waste = cons['Concrete Waste Percent']/100
            else: waste = 0.05

            gross_qty = qty * (1 + waste)
            amount = gross_qty * rate

            boq.append({
                "Section":row['Section'], "Item":row['Item'],
                "Net Qty":qty, "Waste Percent":waste*100,
                "Gross Qty":round(gross_qty,2), "Unit":row['Unit'],
                "Rate":rate, "Amount":round(amount,0)
            })

        df_boq = pd.DataFrame(boq)
        subtotal = df_boq['Amount'].sum()
        vat = subtotal * 0.18
        total = subtotal + vat

        st.dataframe(df_boq, use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Subtotal", f"{subtotal:,.0f} RWF")
        c2.metric("VAT 18%", f"{vat:,.0f} RWF")
        c3.metric("TOTAL", f"{total:,.0f} RWF")

        fig = px.pie(df_boq, values='Amount', names='Section', title="Cost by Section")
        st.plotly_chart(fig, use_container_width=True)

        def to_excel():
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_boq.to_excel(writer, index=False, sheet_name='BOQ')
                st.session_state['materials'].to_excel(writer, index=False, sheet_name='Materials')
            return output.getvalue()

        st.download_button("Download Excel", to_excel(), "B-ESTAMER_4.3.xlsx")

st.divider()
st.caption("B-ESTAMER 4.3 FINAL | All Steel + Brick + Mix Ratios | 0787993679")

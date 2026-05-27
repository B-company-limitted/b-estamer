# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V4.1 - Manual + Auto Takeoff | Contact: 0787993679

import streamlit as st
import pandas as pd
import pdfplumber
import re
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="B-ESTAMER 4.1", layout="wide")
st.title("B-ESTAMER 4.1 AI QUANTITY SURVEYOR 👑")
st.caption("Manual + Auto Takeoff | Outperforming PlanSwift")

# CSS for pro look
st.markdown("""
<style>
   .main {background-color: #0E1117; color: white;}
   .metric-card {background: #1C1F26; padding: 15px; border-radius: 10px; border: 1px solid #2D3748;}
    h1, h2, h3 {color: #FFD700;}
</style>
""", unsafe_allow_html=True)

# Session state init
if 'measurements' not in st.session_state:
    st.session_state['measurements'] = []
if 'materials' not in st.session_state:
    st.session_state['materials'] = pd.DataFrame([
        {"Category":"Structure","Item":"23cm Block","Unit":"pc","Rate":1000},
        {"Category":"Structure","Item":"Cement 42.5N","Unit":"bag","Rate":12500},
        {"Category":"Structure","Item":"Y12 Steel","Unit":"kg","Rate":1300},
        {"Category":"Finishing","Item":"Ceramic Tile","Unit":"m²","Rate":12000},
        {"Category":"MEP","Item":"PPR 20mm","Unit":"m","Rate":2500},
    ])

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Auto Takeoff",
    "✍️ Manual Measure",
    "📊 Materials & Rates",
    "🧮 BOQ",
    "📄 Export"
])

# ===== TAB 1: AUTO TAKEOFF =====
with tab1:
    st.header("Auto Takeoff - Upload PDF")
    uploaded_pdf = st.file_uploader("Upload Architectural PDF", type=["pdf"])

    if uploaded_pdf:
        with pdfplumber.open(uploaded_pdf) as pdf:
            st.success(f"PDF loaded: {len(pdf.pages)} pages")

            # Show first page
            page_img = pdf.pages[0].to_image(resolution=150)
            st.image(page_img.original, use_container_width=True)

            if st.button("🤖 Run Auto Extraction", type="primary"):
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text() + "\n"

                # Auto extraction logic
                extracted = []

                # Extract dimensions like 10.5m, 3.2m
                dims = re.findall(r'(\d+\.?\d*)\s*m', all_text.lower())
                if dims:
                    extracted.append({"Layer":"Walls", "Item":"Wall Length", "Qty":sum(map(float, dims))/2, "Unit":"m"})

                # Extract area like 120m²
                areas = re.findall(r'(\d+\.?\d*)\s*m²', all_text.lower())
                if areas:
                    extracted.append({"Layer":"Slab", "Item":"Floor Area", "Qty":sum(map(float, areas)), "Unit":"m²"})

                # Extract counts like "Door 4", "Window 6"
                doors = len(re.findall(r'door', all_text.lower()))
                windows = len(re.findall(r'window', all_text.lower()))
                if doors:
                    extracted.append({"Layer":"Finishing", "Item":"Doors", "Qty":doors, "Unit":"pc"})
                if windows:
                    extracted.append({"Layer":"Finishing", "Item":"Windows", "Qty":windows, "Unit":"pc"})

                st.session_state['measurements'].extend(extracted)
                st.success(f"Extracted {len(extracted)} items automatically!")

                if extracted:
                    st.dataframe(pd.DataFrame(extracted), use_container_width=True)
    else:
        st.info("Upload PDF to use Auto Takeoff")

# ===== TAB 2: MANUAL MEASURE =====
with tab2:
    st.header("Manual Measurement")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        layer = st.selectbox("Layer", ["Foundation", "Walls", "Slab", "Roof", "Finishing", "MEP"])
    with col2:
        item = st.text_input("Item", "External Wall")
    with col3:
        qty = st.number_input("Quantity", min_value=0.0, step=0.1)
    with col4:
        unit = st.selectbox("Unit", ["m", "m²", "m³", "pc", "kg"])

    if st.button("➕ Add Measurement", use_container_width=True):
        st.session_state['measurements'].append({"Layer":layer, "Item":item, "Qty":qty, "Unit":unit})
        st.rerun()

    if st.session_state['measurements']:
        df_meas = pd.DataFrame(st.session_state['measurements'])
        st.dataframe(df_meas, use_container_width=True, hide_index=True)

        fig = px.bar(df_meas, x='Layer', y='Qty', color='Layer', title="Measurements by Layer")
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🗑️ Clear All"):
            st.session_state['measurements'] = []
            st.rerun()

# ===== TAB 3: MATERIALS =====
with tab3:
    st.header("Materials Database - Full Editable")

    edited = st.data_editor(
        st.session_state['materials'],
        column_config={
            "Rate": st.column_config.NumberColumn("Rate (RWF)", format="%d"),
            "Category": st.column_config.SelectboxColumn(options=["Structure","Finishing","MEP","Substructure"])
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    st.session_state['materials'] = edited

# ===== TAB 4: BOQ =====
with tab4:
    st.header("Bill of Quantities")

    if not st.session_state['measurements']:
        st.warning("Add measurements first in Tab 1 or 2")
    else:
        df_meas = pd.DataFrame(st.session_state['measurements'])
        df_mat = st.session_state['materials']
        rate_map = dict(zip(df_mat['Item'], df_mat['Rate']))

        boq = []
        for _, row in df_meas.iterrows():
            rate = rate_map.get(row['Item'], 5000)
            amount = row['Qty'] * rate
            boq.append({**row, "Rate":rate, "Amount":amount})

        df_boq = pd.DataFrame(boq)
        subtotal = df_boq['Amount'].sum()
        vat = subtotal * 0.18
        total = subtotal + vat

        st.dataframe(df_boq, use_container_width=True, hide_index=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Subtotal", f"{subtotal:,.0f} RWF")
        col2.metric("VAT 18%", f"{vat:,.0f} RWF")
        col3.metric("TOTAL", f"{total:,.0f} RWF")

        fig2 = px.pie(df_boq, values='Amount', names='Layer', title="Cost Distribution")
        st.plotly_chart(fig2, use_container_width=True)

# ===== TAB 5: EXPORT =====
with tab5:
    st.header("Export Report")

    def to_excel():
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if st.session_state['measurements']:
                pd.DataFrame(st.session_state['measurements']).to_excel(writer, index=False, sheet_name='Measurements')
            if 'df_boq' in locals():
                df_boq.to_excel(writer, index=False, sheet_name='BOQ', startrow=3)
                writer.sheets['BOQ'].cell(1,1,"B-ESTAMER 4.1 BOQ Report")
            st.session_state['materials'].to_excel(writer, index=False, sheet_name='Materials')
        return output.getvalue()

    excel_data = to_excel()
    st.download_button(
        "📥 Download Excel Report",
        data=excel_data,
        file_name="B-ESTAMER_4.1_BOQ.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.divider()
st.caption("B-ESTAMER 4.1 | WhatsApp: 0787993679")

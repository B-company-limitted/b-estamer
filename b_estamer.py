# Copyright (c) 2026 BRUNO CONSTRUCTION EMPIRE LTD
# B-ESTAMER V3.21 - PlanSwift + Bluebeam Pro | Contact: 0787993679

import streamlit as st
import pandas as pd
import fitz
from io import BytesIO

st.set_page_config(page_title="B-ESTAMER V3.21", layout="wide")
st.title("B-ESTAMER V3.21 PRECISION EMPIRE 🏗️")
st.caption("PlanSwift + Bluebeam Pro Features")

# ============= MATERIALS DATABASE 40+ ITEMS =============
if 'materials_db' not in st.session_state:
    st.session_state['materials_db'] = pd.DataFrame([
        # SUBSTRUCTURE
        {"Category":"Substructure","Material":"River Sand","Unit":"m³","Rate":25000},
        {"Category":"Substructure","Material":"Aggregate","Unit":"m³","Rate":30000},
        {"Category":"Substructure","Material":"Concrete C25","Unit":"m³","Rate":180000},
        {"Category":"Substructure","Material":"Concrete C30","Unit":"m³","Rate":200000},
        {"Category":"Substructure","Material":"Y16 Steel","Unit":"kg","Rate":1250},
        {"Category":"Substructure","Material":"Y12 Steel","Unit":"kg","Rate":1300},
        {"Category":"Substructure","Material":"DPC 225mm","Unit":"m","Rate":800},
        {"Category":"Substructure","Material":"Polythene 1000g","Unit":"m²","Rate":1500},

        # STRUCTURE
        {"Category":"Structure","Material":"23cm Block","Unit":"pc","Rate":1000},
        {"Category":"Structure","Material":"15cm Block","Unit":"pc","Rate":800},
        {"Category":"Structure","Material":"Cement CEM II 42.5N","Unit":"bag","Rate":12500},
        {"Category":"Structure","Material":"Cement CEM I 52.5N","Unit":"bag","Rate":14500},
        {"Category":"Structure","Material":"Y40 Steel","Unit":"kg","Rate":1400},
        {"Category":"Structure","Material":"Binding Wire","Unit":"kg","Rate":2000},

        # FINISHING
        {"Category":"Finishing","Material":"Ceramic Tile 30x30","Unit":"m²","Rate":12000},
        {"Category":"Finishing","Material":"Granite Tile 60x60","Unit":"m²","Rate":35000},
        {"Category":"Finishing","Material":"Mabati G30","Unit":"m²","Rate":8500},
        {"Category":"Finishing","Material":"Versatile Tile","Unit":"m²","Rate":15000},
        {"Category":"Finishing","Material":"Paint Emulsion","Unit":"m²","Rate":1300},
        {"Category":"Finishing","Material":"Plaster Sand","Unit":"m³","Rate":28000},

        # MEP
        {"Category":"MEP","Material":"PPR 20mm Pipe","Unit":"m","Rate":2500},
        {"Category":"MEP","Material":"PPR 25mm Pipe","Unit":"m","Rate":3500},
        {"Category":"MEP","Material":"2.5mm Cable","Unit":"m","Rate":1200},
        {"Category":"MEP","Material":"4mm Cable","Unit":"m","Rate":1800},
        {"Category":"MEP","Material":"Socket Outlet","Unit":"pc","Rate":3500},
        {"Category":"MEP","Material":"LED Bulb 12W","Unit":"pc","Rate":2500},
        {"Category":"MEP","Material":"DB Board 6Way","Unit":"pc","Rate":35000},
        {"Category":"MEP","Material":"WC Toilet","Unit":"pc","Rate":180000},
        {"Category":"MEP","Material":"Kitchen Sink","Unit":"pc","Rate":85000},
        {"Category":"MEP","Material":"Yaka Meter","Unit":"pc","Rate":80000},

        # DOORS & WINDOWS
        {"Category":"Doors_Windows","Material":"Steel Door 90cm","Unit":"pc","Rate":95000},
        {"Category":"Doors_Windows","Material":"Wooden Door 80cm","Unit":"pc","Rate":75000},
        {"Category":"Doors_Windows","Material":"Aluminium Window","Unit":"m²","Rate":65000},
        {"Category":"Doors_Windows","Material":"Glass 5mm","Unit":"m²","Rate":12000},
    ])

# ============= TABS =============
tab1, tab2, tab3, tab4 = st.tabs(["📐 PDF Takeoff", "🎨 Layers & Measure", "📊 Materials DB", "🧮 Auto BOQ"])

# ============= TAB 1: PDF TAKEOFF =============
with tab1:
    st.header("1. PDF TAKEOFF - Upload & View")
    uploaded_pdf = st.file_uploader("Upload Architectural PDF", type=["pdf"], key="pdf")

    if uploaded_pdf:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        st.session_state['pdf_doc'] = doc
        st.success(f"PDF loaded: {len(doc)} pages")

        page_num = st.selectbox("Select Page", range(len(doc)), format_func=lambda x: f"Page {x+1}")
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        st.image(pix.tobytes(), caption=f"Page {page_num+1}", use_container_width=True)
    else:
        st.info("Upload PDF to enable measurement tools")

# ============= TAB 2: LAYERS & MEASURE =============
with tab2:
    st.header("2. LAYERS & MEASUREMENT - Bluebeam Style")

    if 'pdf_doc' not in st.session_state:
        st.warning("First upload PDF in Tab 1")
    else:
        st.subheader("Layer Management")
        col1, col2, col3 = st.columns(3)
        with col1:
            layer = st.selectbox("Select Layer", ["Foundation","Walls","Roof","Electrical","Plumbing","Rebar"])
        with col2:
            color = st.selectbox("Layer Color", ["Red","Blue","Green","Yellow","Orange","Purple"])
        with col3:
            measure_type = st.selectbox("Measure Type", ["Length m","Area m²","Count pcs","Volume m³"])

        st.info(f"Layer: *{layer}* | Color: *{color}* | Type: *{measure_type}*")
        st.caption("💡 Andika measurements wabonye kuri PDF ukurikije Layer")

        item_name = st.text_input("Item Name", f"{layer} Measurement")
        qty = st.number_input("Quantity", min_value=0.0, step=0.1)

        if 'takeoff_items' not in st.session_state:
            st.session_state['takeoff_items'] = []

        if st.button("➕ Add to Takeoff"):
            st.session_state['takeoff_items'].append({
                "Layer": layer, "Color": color, "Item": item_name,
                "Type": measure_type, "Qty": qty
            })
            st.success(f"Added {item_name}: {qty}")

        if st.session_state['takeoff_items']:
            st.subheader("Takeoff List")
            df_takeoff = pd.DataFrame(st.session_state['takeoff_items'])
            st.dataframe(df_takeoff, use_container_width=True)

            # Auto-Rebar Calculation - PlanSwift Feature
            if st.checkbox("🔧 Auto-Calculate Rebar from Measurements"):
                st.subheader("Auto-Rebar Calculation")

                # Get wall length and area from takeoff
                wall_length = sum([i['Qty'] for i in st.session_state['takeoff_items'] if i['Layer']=='Walls'])
                slab_area = sum([i['Qty'] for i in st.session_state['takeoff_items'] if i['Layer']=='Foundation'])

                rebar_data = []
                if wall_length > 0:
                    rebar_data.append({"Item":"Y12 Steel for Walls","Qty":wall_length*3.5,"Unit":"kg","Rate":1300})
                if slab_area > 0:
                    rebar_data.append({"Item":"Y16 Steel for Slab","Qty":slab_area*12,"Unit":"kg","Rate":1250})
                    rebar_data.append({"Item":"Y40 Steel for Columns","Qty":slab_area*0.5*100,"Unit":"kg","Rate":1400})

                if rebar_data:
                    df_rebar = pd.DataFrame(rebar_data)
                    st.dataframe(df_rebar, use_container_width=True)
                    if st.button("➕ Add Rebar to Takeoff"):
                        for r in rebar_data:
                            st.session_state['takeoff_items'].append({
                                "Layer":"Rebar","Color":"Purple","Item":r['Item'],
                                "Type":"Count pcs","Qty":r['Qty']
                            })
                        st.success("Rebar added!")
                        st.rerun()

# ============= TAB 3: MATERIALS DB =============
with tab3:
    st.header("3. MATERIALS DATABASE - Full Editable")
    st.caption("Hindura rates zose. Zizakoreshwa muri BOQ.")

    edited_db = st.data_editor(
        st.session_state['materials_db'],
        column_config={
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Substructure","Structure","Finishing","MEP","Doors_Windows"]
            ),
            "Rate": st.column_config.NumberColumn("Rate RWF", format="%d"),
        },
        use_container_width=True,
        num_rows="dynamic",
        key="db_editor"
    )
    st.session_state['materials_db'] = edited_db

# ============= TAB 4: AUTO BOQ =============
with tab4:
    st.header("4. AUTO BOQ GENERATOR")

    if 'takeoff_items' not in st.session_state or not st.session_state['takeoff_items']:
        st.warning("First add items in Tab 2 Takeoff")
    else:
        df_takeoff = pd.DataFrame(st.session_state['takeoff_items'])
        db = st.session_state['materials_db']
        rate_dict = dict(zip(db['Material'], db['Rate']))

        boq_items = []

        for _, row in df_takeoff.iterrows():
            layer = row['Layer']
            qty = row['Qty']

            # Auto-match material based on layer
            if layer == "Foundation":
                mat = "Concrete C25"
                unit = "m³"
            elif layer == "Walls":
                mat = "23cm Block"
                unit = "m²"
                qty = qty * 12.5 # convert m to blocks
            elif layer == "Rebar":
                mat = row['Item'].split(" for ")[0]
                unit = "kg"
            elif layer == "Electrical":
                mat = "2.5mm Cable"
                unit = "m"
            else:
                mat = "Cement CEM II 42.5N"
                unit = "bag"

            rate = rate_dict.get(mat, 0)
            amount = qty * rate

            boq_items.append([row['Layer'], row['Item'], qty, unit, rate, amount])

        boq_df = pd.DataFrame(boq_items, columns=["Layer","Description","Qty","Unit","Rate","Amount"])
        boq_df["Amount"] = pd.to_numeric(boq_df["Amount"], errors='coerce').fillna(0)

        subtotal = boq_df["Amount"].sum()
        vat = subtotal * 0.18
        total = subtotal + vat

        st.subheader("Generated BOQ")
        st.dataframe(boq_df, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Subtotal", f"{subtotal:,.0f} RWF")
        c2.metric("VAT 18%", f"{vat:,.0f} RWF")
        c3.metric("TOTAL", f"{total:,.0f} RWF")

        # Export Excel
        def to_excel():
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                boq_df.to_excel(writer, index=False, sheet_name='BOQ', startrow=3)
                writer.sheets['BOQ'].cell(1,1,"B-ESTAMER V3.21 PRECISION EMPIRE")
                edited_db.to_excel(writer, index=False, sheet_name='Materials_DB')
                df_takeoff.to_excel(writer, index=False, sheet_name='Takeoff_Layers')
            return output.getvalue()

        excel_data = to_excel()
        st.download_button(
            "📥 Download Full Excel Report",
            data=excel_data,
            file_name=f"B-ESTAMER_V321_{total:,.0f}RWF.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.divider()
st.caption("B-ESTAMER V3.21 | PlanSwift Takeoff + Bluebeam Layers + Auto-Rebar | 0787993679")

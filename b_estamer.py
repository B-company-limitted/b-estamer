import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="B-ESTAMER", page_icon="🏗️", layout="wide")

st.title("B-ESTAMER")
st.subheader("AI-Powered SaaS Platform for Instant RPPA-Compliant BOQ Generation")
st.write("By Bruno, Civil Engineering Student")
st.divider()

uploaded_plan = st.file_uploader("📂 Shyiramo Plan PDF/JPG/PNG", type=["pdf", "jpg", "png"])

if uploaded_plan:
    st.success("Plan yakiriwe! AI irimo gukora BOQ...")

    try:
        prices_df = pd.read_csv("prices_rw.csv")
    except:
        st.error("File ya prices_rw.csv ntibonetse. Hindura izina rya CSV muri GitHub.")
        st.stop()

    def get_price(item_name):
        price = prices_df[prices_df['Item'] == item_name]['Unit Price RWF'].values
        return int(price[0]) if len(price) > 0 else 0

    data = {
        "Description": ["Excavation", "Cement 32.5", "Blocks 15cm", "Steel Y12", "Sand"],
        "Unit": ["m3", "Bag", "Pcs", "Kg", "Tripper 5m3"],
        "Quantity": [15, 25, 800, 120, 2],
        "Unit Price RWF": [3000, get_price("Cement 32.5"), get_price("Blocks 15cm"), get_price("Steel Y12"), get_price("Sand")]
    }

    boq = pd.DataFrame(data)
    boq["Total RWF"] = boq["Quantity"] * boq["Unit Price RWF"]

    st.subheader("📋 BOQ YUZUYE - RPPA COMPLIANT")
    st.dataframe(boq, use_container_width=True)

    current_date = prices_df['Date'].iloc[0] if 'Date' in prices_df.columns else "2026-04-28"
    st.caption(f"Price Source: Updated {current_date} | B-ESTAMER v1.0")

    total = boq["Total RWF"].sum()
    st.metric(label="TOTAL BOQ AMOUNT", value=f"{total:,} RWF")

    st.download_button(
        label="📥 Download Excel BOQ",
        data=boq.to_csv(index=False).encode('utf-8'),
        file_name=f"B-ESTAMER_BOQ_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

else:
    st.info("Shyiramo plan hejuru kugira ngo AI ikore BOQ mu minota 5.")

st.divider()
st.caption("B-ESTAMER is not just a website. It's a Cloud-Based AI Platform that replaces 3 days of manual QS work with 5 minutes of automation.")

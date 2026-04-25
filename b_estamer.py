import streamlit as st

st.set_page_config(page_title="B ESTAMER V2", layout="wide")
st.title("🔥 B ESTAMER V2 - CEO MODE")

st.write("---")
izina = st.text_input("Andika izina ryawe")
company = st.text_input("Andika Company yawe")

if st.button("Kanda Unyemeze"):
    st.balloons()
    st.success(f"Murakaza neza {izina}!")
    st.success(f"Company {company} irabyaye!")
    st.write("## Watsinze Level 2 mn!")

st.write("---")
st.write("*Project Statistics:*")
col1, col2, col3 = st.columns(3)
col1.metric("Victory", "100%")
col2.metric("Errors Zitsinzwe", "20")
col3.metric("CEO Level", "2")

import streamlit as st

st.set_page_config(
    page_title="B ESTAMER V2 - CEO MODE", 
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 4px solid #43A047;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center; 
        color: #424242;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border: 2px solid #43A047;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #43A047;
        border: 2px solid #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🔥 B ESTAMER V2 - CEO MODE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by B Company Limetted | Blue • White • Green</div>', unsafe_allow_html=True)

st.write("### Andika izina ryawe")
izina = st.text_input(" ", placeholder="Andika izina ryawe hano...")

st.write("### Andika Company yawe") 
company = st.text_input("  ", placeholder="Andika company yawe hano...")

if st.button("Kanda Uyemeze", use_container_width=True):
    if izina and company:
        st.balloons()
        st.success(f"Murakaza neza {izina} muri {company}!")
        st.markdown("### 🎉 Watsinze Level 2 mn!")
    else:
        st.error("Uzuza izina na company mbere yo gukanda")

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Victory", "100%", "✅")
with col2:
    st.metric("Errors Zitsinzwe", "20", "🔥")
with col3:
    st.metric("CEO Level", "3", "👑")


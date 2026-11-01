
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="CAMPLAB",
    page_icon="⚛️",
    layout="wide"
)

# ESTIL VISUAL
st.markdown("""
<style>
.stApp {
    background-color: #101D2B;
}
h1 {
    color: #42D9F5;
}
h2, h3 {
    color: #FFFFFF;
}
p, label {
    color: #C4D5E3;
}
[data-testid="stSidebar"] {
    background-color: #172A3B;
}
</style>
""", unsafe_allow_html=True)

# CAPÇALERA
st.title("CAMPLAB")
st.caption("LABORATORI VIRTUAL DE PARTÍCULES I CAMPS ELECTROMAGNÈTICS")

st.markdown("---")

# BARRA LATERAL
st.sidebar.title("Configuració")

particula = st.sidebar.selectbox(
    "Partícula",
    ["Protó", "Electró", "Positró"]
)

tipus_camp = st.sidebar.selectbox(
    "Tipus de camp",
    [
        "Camp elèctric",
        "Camp magnètic",
        "Camps electromagnètics"
    ]
)

intensitat = st.sidebar.slider(
    "Intensitat del camp",
    0.0, 2.0, 1.0, 0.1
)

velocitat = st.sidebar.number_input(
    "Velocitat inicial (m/s)",
    min_value=1000,
    max_value=10000000,
    value=1000000
)

# PRESENTACIÓ
st.subheader("Laboratori de simulació")

st.write(
    "Configura les propietats de les partícules "
    "i els camps electromagnètics per estudiar-ne "
    "el moviment."
)

# INFORMACIÓ
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Partícula", particula)

with col2:
    st.metric("Camp seleccionat", tipus_camp)

with col3:
    st.metric("Velocitat inicial", f"{velocitat:.2e} m/s")

st.markdown("---")

st.subheader("Paràmetres de l'experiment")

st.write(f"Intensitat seleccionada: {intensitat:.1f}")

st.info(
    "Configura els paràmetres a la barra lateral. "
    "La simulació interactiva s'afegirà a continuació."
)

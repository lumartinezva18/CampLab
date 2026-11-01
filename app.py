
import streamlit as st

# Configuració de la pàgina
st.set_page_config(
    page_title="CAMPLAB",
    page_icon="⚛️",
    layout="wide"
)

# Estil visual
st.markdown("""
<style>
.stApp {
    background-color: #101D2B;
    color: #FFFFFF;
}
h1 {
    color: #42D9F5;
}
</style>
""", unsafe_allow_html=True)

# Capçalera
st.title("CAMPLAB")
st.subheader("Laboratori virtual de partícules i camps electromagnètics")

st.markdown("---")

st.write(
    "Explora el moviment de partícules carregades "
    "mitjançant simulacions de camps elèctrics i magnètics."
)

st.info("Benvingut/da a CAMPLAB. El laboratori està en desenvolupament.")

st.markdown("### Selecció de partícules")

particula = st.selectbox(
    "Escull una partícula:",
    ["Protó", "Electró", "Positró"]
)

st.write(f"Partícula seleccionada: **{particula}**")

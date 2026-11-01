
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURACIÓ
st.set_page_config(
    page_title="CAMPLAB",
    page_icon="⚛️",
    layout="wide"
)

# CONSTANTS FÍSIQUES
e = 1.602176634e-19
m_e = 9.1093837139e-31
m_p = 1.67262192595e-27

particules = {
    "Protó": {"q": e, "m": m_p},
    "Electró": {"q": -e, "m": m_e},
    "Positró": {"q": e, "m": m_e}
}

# ESTIL
st.markdown("""
<style>
.stApp {background-color: #101D2B;}
h1 {color: #42D9F5;}
h2, h3 {color: white;}
p, label {color: #C4D5E3;}
[data-testid="stSidebar"] {background-color: #172A3B;}
</style>
""", unsafe_allow_html=True)

# MOTOR DE SIMULACIÓ
def simular_particula(nom, v0, E, B, T, N):
    q = particules[nom]["q"]
    m = particules[nom]["m"]

    t = np.linspace(0, T, N)
    dt = t[1] - t[0]

    estat = np.zeros((N, 4))
    estat[0] = [0, 0, v0, 0]

    def derivada(s):
        x, y, vx, vy = s
        ax = (q/m) * (E + vy*B)
        ay = (q/m) * (-vx*B)
        return np.array([vx, vy, ax, ay])

    for i in range(N-1):
        s = estat[i]

        k1 = derivada(s)
        k2 = derivada(s + dt*k1/2)
        k3 = derivada(s + dt*k2/2)
        k4 = derivada(s + dt*k3)

        estat[i+1] = s + dt*(k1 + 2*k2 + 2*k3 + k4)/6

    x, y, vx, vy = estat.T
    energia = 0.5*m*(vx**2 + vy**2)

    return t, x, y, energia

# CAPÇALERA
st.title("CAMPLAB")
st.caption("LABORATORI VIRTUAL DE PARTÍCULES I CAMPS ELECTROMAGNÈTICS")
st.markdown("---")

# CONTROLS
st.sidebar.title("Configuració de l'experiment")

nom = st.sidebar.selectbox(
    "Partícula",
    list(particules.keys())
)

tipus = st.sidebar.selectbox(
    "Tipus de camp",
    ["Camp elèctric", "Camp magnètic", "Camps combinats"]
)

intensitat_E = st.sidebar.number_input(
    "Camp elèctric (N/C)",
    min_value=0.0,
    value=1000.0,
    step=100.0
)

intensitat_B = st.sidebar.number_input(
    "Camp magnètic (T)",
    min_value=0.0,
    value=0.001,
    format="%.5f"
)

v0 = st.sidebar.number_input(
    "Velocitat inicial (m/s)",
    min_value=1000,
    max_value=10000000,
    value=1000000
)

T = st.sidebar.number_input(
    "Temps de simulació (s)",
    min_value=1e-10,
    max_value=1e-6,
    value=1e-8,
    format="%.2e"
)

# SELECCIÓ DEL CAMP
if tipus == "Camp elèctric":
    E = intensitat_E
    B = 0

elif tipus == "Camp magnètic":
    E = 0
    B = intensitat_B

else:
    E = intensitat_E
    B = intensitat_B

# SIMULACIÓ
st.subheader("Simulació de trajectòries")

if st.button("Executar simulació", type="primary"):

    t, x, y, energia = simular_particula(
        nom, v0, E, B, T, 2000
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Energia inicial", f"{energia[0]:.3e} J")

    with col2:
        st.metric("Energia final", f"{energia[-1]:.3e} J")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, y, color="#00BFEA")
    ax.set_xlabel("Posició X (m)")
    ax.set_ylabel("Posició Y (m)")
    ax.set_title(f"Trajectòria del {nom.lower()}")
    ax.grid(True)
    ax.set_aspect("equal", adjustable="datalim")

    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(9, 4))
    ax2.plot(t, energia, color="#42D9F5")
    ax2.set_xlabel("Temps (s)")
    ax2.set_ylabel("Energia cinètica (J)")
    ax2.set_title("Evolució de l'energia cinètica")
    ax2.grid(True)

    st.pyplot(fig2)

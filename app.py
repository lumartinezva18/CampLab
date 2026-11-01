
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# CONFIGURACIÓ
st.set_page_config(
    page_title="CAMPLAB",
    page_icon="⚛️",
    layout="wide")

# NAVEGACIÓ PRINCIPAL
tab1, tab2, tab3, tab4 = st.tabs([
    "⌂  Pàgina inicial",
    "⚙  Simulació",
    "◎  Visualització",
    "▥  Anàlisi"
])

# CONSTANTS FÍSIQUES
e = 1.602176634e-19
m_e = 9.1093837139e-31
m_p = 1.67262192595e-27
particules = {
    "Protó": {"q": e, "m": m_p},
    "Electró": {"q": -e, "m": m_e},
    "Positró": {"q": e, "m": m_e}}

# ESTIL
st.markdown("""
<style>
/* FONS */
.stApp {
    background: #0D1723;
    color: #E7EDF4;
}
.block-container {
    max-width: 1450px;
    padding-top: 5rem;
    padding-bottom: 3rem;
}
/* TIPOGRAFIA */
h1 {
    color: #55C5DF !important;
    font-size: 2.8rem !important;
    font-weight: 750 !important;
    letter-spacing: 2px;}
h2, h3 {
    color: #EAF1F7 !important;
    font-weight: 600 !important;}
p, label {
    color: #AEBECD;
}

/* TARGETES */
[data-testid="stMetric"] {
    background: #172635;
    border: 1px solid #293E50;
    border-radius: 12px;
    padding: 20px;
}
[data-testid="stMetricValue"] {
    color: #55C5DF !important;
}
[data-testid="stMetricLabel"] {
    color: #AEBECD !important;
}

/* BOTONS */
.stButton > button {
    background: #167F9B;
    color: white;
    border: 1px solid #249BB8;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.65rem 1.2rem;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #239BB8;
    border-color: #55C5DF;
    color: white;
}

/* SELECTORS */
.stSelectbox > div > div,
.stNumberInput > div > div {
    background: #172635;
    border-radius: 8px;
}

/* GRAFICS */
[data-testid="stImage"],
[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"] {
    border-radius: 12px;
}
/* SEPARADORS */
hr {
    border-color: #293E50;
}
/* MISSATGES */
[data-testid="stAlert"] {
    background: #172635;
    border: 1px solid #293E50;
    border-radius: 10px;
}

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


# DASHBOARD

with tab1:
    st.title("CAMPLAB")
    st.subheader("Computational Analysis of Motion and Particle Laboratory")

    st.markdown("""
    ### Laboratori virtual de física de partícules

    CAMPLAB és una aplicació interactiva que permet estudiar
    el moviment de partícules carregades sotmeses a camps
    elèctrics i magnètics.

    **Objectius del laboratori:**
    - Simular trajectòries de diferents partícules.
    - Comparar el comportament del protó, l'electró i el positró.
    - Analitzar la influència dels camps electromagnètics.
    - Estudiar els canvis en l'energia cinètica.
    """)

    st.divider()

    st.caption("CAMPLAB · Simulació computacional de física")

# PESTANYA DE SIMULACIÓ

with tab2:
    st.title("Simulació de partícules")
    st.markdown(
        "Configura les condicions inicials i observa el moviment "
        "de les partícules carregades."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Partícula")
        nom = st.selectbox(
            "Selecciona la partícula",
            ["Protó", "Electró", "Positró"]
        )

        v0 = st.number_input(
            "Velocitat inicial (m/s)",
            min_value=0.0,
            value=1000000.0,
            step=100000.0
        )

    with col2:
        st.subheader("Camp electromagnètic")
        tipus = st.selectbox(
            "Tipus de camp",
            ["Camp elèctric", "Camp magnètic", "Camps combinats"]
        )

        intensitat_E = st.number_input(
            "Intensitat del camp elèctric (N/C)",
            min_value=0.0,
            value=1000.0
        )

        intensitat_B = st.number_input(
            "Intensitat del camp magnètic (T)",
            min_value=0.0,
            value=0.001,
            format="%.6f"
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        T = st.number_input(
            "Temps de simulació (s)",
            min_value=0.000000001,
            value=0.0000005,
            format="%.8e"
        )

    with col4:
        N = st.number_input(
            "Nombre de passos temporals",
            min_value=100,
            max_value=20000,
            value=5000,
            step=500
        )

    if tipus == "Camp elèctric":
        E = intensitat_E
        B = 0.0
    elif tipus == "Camp magnètic":
        E = 0.0
        B = intensitat_B
    else:
        E = intensitat_E
        B = intensitat_B

    st.divider()

    executar = st.button(
        "Executar simulació",
        type="primary",
        use_container_width=True
    )

    if executar:
        t, x, y, energia = simular_particula(
            nom, v0, E, B, T, int(N)
        )

        st.success("Simulació completada!")

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(x, y, label=nom, linewidth=2)
        ax.set_xlabel("Posició X (m)")
        ax.set_ylabel("Posició Y (m)")
        ax.set_title("Trajectòria de la partícula")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(t, energia, linewidth=2)
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Energia cinètica (J)")
        ax.set_title("Evolució de l'energia cinètica")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)

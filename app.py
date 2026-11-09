
import streamlit as st
import numpy as np

from simulació.nucli_físic import simular_3d

from visualització.animació_3d import animacio_3d

from visualització.gràfiques import (
    crear_grafica,
    crear_projeccions
)

from simulació.partícules import particules
from simulació.mètode_numèric import rk4


# =====================================================
# 1. CONFIGURACIÓ
# =====================================================

st.set_page_config(
    page_title="CAMPLAB",
    page_icon="⚛️",
    layout="wide"
)


# =====================================================
# 2. ESTIL
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #0D1723;
    color: #E7EDF4;
}

.block-container {
    max-width: 1500px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

h1 {
    color: #55C5DF !important;
    font-size: 2.8rem !important;
    font-weight: 750 !important;
    letter-spacing: 2px;
}

h2, h3 {
    color: #EAF1F7 !important;
}

p, label {
    color: #AEBECD;
}

[data-testid="stMetric"] {
    background: #172635;
    border: 1px solid #293E50;
    border-radius: 12px;
    padding: 20px;
}

[data-testid="stMetricValue"] {
    color: #55C5DF !important;
}

.stButton > button {
    background: #167F9B;
    color: white;
    border: 1px solid #249BB8;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #239BB8;
    color: white;
}

hr {
    border-color: #293E50;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. NAVEGACIÓ
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "⌂  Pàgina inicial",
    "⚙  Simulació",
    "◎  Visualització",
    "▥  Anàlisi"
])


# =====================================================
# 4. PÀGINA INICIAL
# =====================================================

with tab1:

    st.title("CAMPLAB")

    st.subheader(
        "Darrere la trajectòria: explora l'invisible als ulls"
    )

    st.markdown("""
    ### Laboratori virtual de física de partícules

    CAMPLAB és una aplicació interactiva que permet estudiar
    el moviment tridimensional de partícules carregades
    sotmeses a camps elèctrics i magnètics.

    **Objectius del laboratori:**

    - Simular trajectòries tridimensionals.
    - Comparar el protó, l'electró i el positró.
    - Analitzar la influència dels camps electromagnètics.
    - Estudiar l'evolució de la velocitat i l'energia cinètica.
    """)

    st.divider()

    st.caption("CAMPLAB · Laboratori virtual de física")


# =====================================================
# 5. SIMULACIÓ
# =====================================================

with tab2:

    st.title("LABORATORI DE SIMULACIONS")

    st.caption(
        "Configura les condicions inicials de l'experiment."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("PARTICULA")

        nom = st.selectbox(
            "Selecciona la partícula",
            ["Protó", "Electró", "Positró"]
        )

        st.markdown("**Components de la velocitat incial**")

        vx0 = st.number_input(
            "Vx (m/s)",
            value=1000000.0,
            format="%.3e"
        )

        vy0 = st.number_input(
            "Vy (m/s)",
            value=0.0,
            format="%.3e"
        )

        vz0 = st.number_input(
            "Vz (m/s)",
            value=0.0,
            format="%.3e"
        )

    with col2:

        st.subheader("CAMP ELECTROMAGNÈTIC")

        tipus = st.selectbox(
            "Tipus de camp",
            [
                "Camp elèctric",
                "Camp magnètic",
                "Camps combinats"
            ]
        )

        st.markdown("**Camp Elèctric (N/C)**")

        ex = st.number_input("Ex", value=1000.0)
        ey = st.number_input("Ey", value=0.0)
        ez = st.number_input("Ez", value=0.0)

        st.markdown("**Camp magnètic (T)**")

        bx = st.number_input("Bx", value=0.0)
        by = st.number_input("By", value=0.0)
        bz = st.number_input(
            "Bz",
            value=0.001,
            format="%.6f"
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        T = st.number_input(
            "Temps de simulació (s)",
            min_value=1e-12,
            value=5e-7,
            format="%.3e"
        )

    with col4:

        N = st.number_input(
            "Número de passos temporals",
            min_value=100,
            max_value=20000,
            value=5000,
            step=500
        )

    st.divider()

    executar = st.button(
        "▶ EXECUTAR",
        type="primary",
        use_container_width=True
    )

    # Camps electromagnètics
    E = np.array([ex, ey, ez], dtype=float)
    B = np.array([bx, by, bz], dtype=float)

    if tipus == "Camp elèctric":
        B = np.zeros(3)

    elif tipus == "Camp magnètic":
        E = np.zeros(3)

    # Velocitat inicial
    v0 = np.array(
        [vx0, vy0, vz0],
        dtype=float
    )

    # Execució
    if executar:

        if np.linalg.norm(v0) == 0:

            st.error(
                "La velocitat inicial no pot ser zero."
            )

        else:

            resultat = simular_3d(
                nom,
                v0,
                E,
                B,
                T,
                int(N)
            )

            st.session_state["resultat"] = resultat

            st.success(
                "Simulació completada correctament!"
            )

    # Resultats
    if "resultat" in st.session_state:

        resultat = st.session_state["resultat"]

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Velocitat final",
                f"{resultat['velocitat'][-1]:.3e} m/s"
            )

        with col2:

            st.metric(
                "Energia inicial",
                f"{resultat['energia'][0]:.3e} J"
            )

        with col3:

            st.metric(
                "Energia final",
                f"{resultat['energia'][-1]:.3e} J"
            )


# =====================================================
# 6. VISUALITZACIÓ 3D
# =====================================================

with tab3:

    st.title("VISUALITZACIÓ 3D")

    st.caption(
        "Representació tridimensional del moviment de la partícula."
    )

    if "resultat" in st.session_state:

        resultat = st.session_state["resultat"]

        st.subheader(
            f"Trajectòria del {resultat['nom'].lower()}"
        )

        fig = animacio_3d(resultat)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "scrollZoom": True
            }
        )

        st.caption(
            "Arrossega el ratolí per rotar la vista "
            "i utilitza la roda per ampliar o allunyar."
        )

    else:

        st.info(
            "Executa primer una simulació per visualitzar "
            "la trajectòria tridimensional."
        )


# =====================================================
# 7. ANÀLISI
# =====================================================

with tab4:

    st.title("ANÀLISI DELS RESULTATS")

    if "resultat" in st.session_state:

        resultat = st.session_state["resultat"]

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Velocitat en front de temps")

            fig = crear_grafica(
                resultat["t"],
                resultat["velocitat"],
                "Velocitat/temps",
                "Velocitat (m/s)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader("Energia cinètica en front de temps")

            fig = crear_grafica(
                resultat["t"],
                resultat["energia"],
                "Energia cinètica/temps",
                "Energia (J)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("Acceleració en front de temps")

        fig = crear_grafica(
            resultat["t"],
            resultat["acceleracio"],
            "Acceleració/temps",
            "Acceleració (m/s²)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Projecció de la trajectòria")

        fig = crear_projeccions(resultat)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Executa una simulació per consultar-ne els resultats."
        )


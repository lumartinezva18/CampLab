
# CONSTANTS PHYSIQUES

e = 1.602176634e-19

m_e = 9.1093837139e-31

m_p = 1.67262192595e-27


# PARTICLES

particules = {
    "Protó": {
        "q": e,
        "m": m_p
    },

    "Electró": {
        "q": -e,
        "m": m_e
    },

    "Positró": {
        "q": e,
        "m": m_e
    }
}

# MÈTODES NUMÈRICS

import numpy as np


def rk4(derivada, estat_inicial, t):

    N = len(t)
    dt = t[1] - t[0]

    estat = np.zeros((N, len(estat_inicial)))

    estat[0] = estat_inicial

    for i in range(N - 1):

        s = estat[i]

        k1 = derivada(s)
        k2 = derivada(s + dt * k1 / 2)
        k3 = derivada(s + dt * k2 / 2)
        k4 = derivada(s + dt * k3)

        estat[i + 1] = s + (dt / 6) * (
            k1 + 2*k2 + 2*k3 + k4
        )

    return estat

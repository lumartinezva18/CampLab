
import numpy as np

from simulation.particles import particules
from simulation.numerical_methods import rk4


def simular_3d(nom, v0, E, B, T, N):

    q = particules[nom]["q"]
    m = particules[nom]["m"]

    t = np.linspace(0, T, N)

    # Condicions inicials
    estat_inicial = np.array([
        0, 0, 0,
        v0[0], v0[1], v0[2]
    ], dtype=float)

    # Equacions diferencials
    def derivada(s):

        posicio = s[:3]
        velocitat = s[3:]

        acceleracio = (q / m) * (
            E + np.cross(velocitat, B)
        )

        return np.concatenate((
            velocitat,
            acceleracio
        ))

    # Integració RK4
    estat = rk4(
        derivada,
        estat_inicial,
        t
    )

    # Posicions
    x = estat[:, 0]
    y = estat[:, 1]
    z = estat[:, 2]

    # Velocitats
    vx = estat[:, 3]
    vy = estat[:, 4]
    vz = estat[:, 5]

    # Acceleracions
    acceleracio = np.array([
        derivada(s)[3:]
        for s in estat
    ])

    ax = acceleracio[:, 0]
    ay = acceleracio[:, 1]
    az = acceleracio[:, 2]

    # Mòduls
    velocitat = np.sqrt(
        vx**2 + vy**2 + vz**2
    )

    acceleracio_modul = np.sqrt(
        ax**2 + ay**2 + az**2
    )

    # Energia cinètica
    energia = 0.5 * m * velocitat**2

    return {
        "t": t,
        "x": x,
        "y": y,
        "z": z,

        "vx": vx,
        "vy": vy,
        "vz": vz,

        "ax": ax,
        "ay": ay,
        "az": az,

        "velocitat": velocitat,
        "acceleracio": acceleracio_modul,
        "energia": energia,

        "nom": nom,
        "massa": m,
        "carrega": q
    }

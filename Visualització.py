
import plotly.graph_objects as go


def animacio_3d(resultat):

    x = resultat["x"]
    y = resultat["y"]
    z = resultat["z"]

    nom = resultat["nom"]

    # Selecció dels fotogrames
    pas = max(1, len(x) // 120)

    indices = list(range(0, len(x), pas))

    if indices[-1] != len(x) - 1:
        indices.append(len(x) - 1)

    fig = go.Figure()

    # Trajectòria completa de referència
    fig.add_trace(go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="lines",
        line=dict(
            color="rgba(85,197,223,0.20)",
            width=3
        ),
        name="Trajectòria completa"
    ))

    # Rastre
    fig.add_trace(go.Scatter3d(
        x=[x[0]],
        y=[y[0]],
        z=[z[0]],
        mode="lines",
        line=dict(
            color="#00DFFF",
            width=6
        ),
        name="Rastre"
    ))

    # Partícula
    fig.add_trace(go.Scatter3d(
        x=[x[0]],
        y=[y[0]],
        z=[z[0]],
        mode="markers",
        marker=dict(
            size=8,
            color="#55E8FF",
            line=dict(
                color="white",
                width=1
            )
        ),
        name=nom
    ))

    # Fotogrames de l'animació
    frames = []

    for i in indices:

        frames.append(go.Frame(
            name=str(i),

            data=[
                go.Scatter3d(
                    x=x[:i+1],
                    y=y[:i+1],
                    z=z[:i+1]
                ),

                go.Scatter3d(
                    x=[x[i]],
                    y=[y[i]],
                    z=[z[i]]
                )
            ],

            traces=[1, 2]
        ))

    fig.frames = frames

    # Disseny
    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0D1723",
        plot_bgcolor="#0D1723",

        height=680,

        title=dict(
            text="3D PARTICLE TRAJECTORY",
            font=dict(
                color="#55C5DF",
                size=20
            )
        ),

        scene=dict(

            bgcolor="#0D1723",

            xaxis=dict(
                title="X (m)",
                gridcolor="#293E50"
            ),

            yaxis=dict(
                title="Y (m)",
                gridcolor="#293E50"
            ),

            zaxis=dict(
                title="Z (m)",
                gridcolor="#293E50"
            ),

            aspectmode="data"
        ),

        margin=dict(
            l=0,
            r=0,
            b=0,
            t=60
        ),

        # Controls de reproducció
        updatemenus=[dict(

            type="buttons",
            showactive=False,

            buttons=[

                dict(
                    label="▶ PLAY",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {
                                "duration": 25,
                                "redraw": True
                            },
                            "fromcurrent": True,
                            "transition": {
                                "duration": 0
                            }
                        }
                    ]
                ),

                dict(
                    label="Ⅱ PAUSE",
                    method="animate",
                    args=[
                        [None],
                        {
                            "mode": "immediate",
                            "frame": {
                                "duration": 0,
                                "redraw": False
                            }
                        }
                    ]
                )
            ]
        )],

        # Barra temporal
        sliders=[dict(

            active=0,

            currentvalue=dict(
                prefix="Frame: "
            ),

            steps=[

                dict(
                    method="animate",

                    args=[
                        [str(i)],
                        {
                            "mode": "immediate",
                            "frame": {
                                "duration": 0,
                                "redraw": True
                            }
                        }
                    ],

                    label=str(j)
                )

                for j, i in enumerate(indices)
            ]
        )]
    )

    return fig

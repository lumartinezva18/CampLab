
import plotly.graph_objects as go


def crear_grafica(t, valores, titol, eix_y):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=valores,
        mode="lines",
        line=dict(
            color="#55C5DF",
            width=2
        )
    ))

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0D1723",
        plot_bgcolor="#172635",

        title=titol,

        xaxis_title="Temps (s)",
        yaxis_title=eix_y,

        height=400,

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=40
        )
    )

    return fig


def crear_projeccions(resultat):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=resultat["x"],
        y=resultat["y"],
        mode="lines",
        name="XY"
    ))

    fig.add_trace(go.Scatter(
        x=resultat["x"],
        y=resultat["z"],
        mode="lines",
        name="XZ"
    ))

    fig.add_trace(go.Scatter(
        x=resultat["y"],
        y=resultat["z"],
        mode="lines",
        name="YZ"
    ))

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0D1723",
        plot_bgcolor="#172635",

        title="Projeccions de la trajectòria",

        xaxis_title="Posició (m)",
        yaxis_title="Posició (m)",

        height=450
    )

    return fig

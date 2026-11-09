
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



from plotly.subplots import make_subplots


def crear_projeccions(resultat):

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("PLÀ XY", "PLÀ XZ", "PLÀ YZ")
    )

    plans = [
        (resultat["x"], resultat["y"], 1),
        (resultat["x"], resultat["z"], 2),
        (resultat["y"], resultat["z"], 3)
    ]

    for x, y, columna in plans:

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(
                    color="#55C5DF",
                    width=2
                ),
                showlegend=False
            ),
            row=1,
            col=columna
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1723",
        plot_bgcolor="#172635",
        height=430,
        title="Projeccions bidimensionals de la trajectòria"
    )

    return fig


    

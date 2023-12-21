import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

dash1 = Dash(requests_pathname_prefix="/dash/app1/",external_stylesheets=[dbc.themes.BOOTSTRAP])

dash1.title = "大安捷運站出口-Youbike站點車輛訊息"

dash1.layout = html.Div([
    html.H1('        Youbike站點車輛訊息'),
    dcc.Graph(id='graph'),
    
])

@dash1.callback(
    Output("graph", "figure"),
    Input("graph", "id")
)
def update_line_chart(station):
    df = pd.read_csv('./dash_file/Youbike1221_4.csv')
    fig = px.line(df, x="status", y="number", color='station',text='number')
    fig.update_traces(textposition="bottom right")

    return fig

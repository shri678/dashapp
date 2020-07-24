import plotly.express as px
from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Load Data
url = 'https://raw.githubusercontent.com/dirkkoolmees/CO2_emissions_per-region/master/CO2%20Emissions%20per%20region%20-%20Sheet2.csv'
df = pd.read_csv(url, index_col = 'Year')

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H3("CO2 Emissions from fossil fuels and cement production"),
        html.Div([
        dcc.Dropdown(
            id='region', clearable=False,
            value='North America', options=[
                {'label': c, 'value': c}
                for c in df.columns
            ], multi = True),
    ],style={'display': 'inline', 'width': '15%'}),
        
        html.Div([
        dcc.Graph(id='graph'),
    ],style={'display': 'inline-block', 'width': '45%'}),
        
        html.Div([
        dcc.Graph(id='graph_2'),
    ],style={'display': 'inline-block', 'width': '55%'})
])
# Define callback to update graph
@app.callback(
    [Output('graph', 'figure'),Output('graph_2', 'figure')],
    [Input("region", "value")]
)

def multi_output(region):
    if region is None:
        raise PreventUpdate

    fig1 = px.line(df, x=df.index, y=region)
    fig2 = px.area(df, x=df.index, y=region)
    
    fig1.update_layout(
    yaxis_title='Thousand metric tons of C',
    showlegend = False
    )
    
    fig2.update_layout(
    legend_title_text='Region',
    yaxis_title='Thousand metric tons of C',
    )

    fig1.update_xaxes(showspikes=True)
    fig1.update_yaxes(showspikes=True)

    return fig1, fig2




# Run app
if __name__ == '__main__':
    app.run_server(debug = True)

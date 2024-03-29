# Dicas de templates: https://pypi.org/project/dash-bootstrap-templates/

# dockerizacao: https://python.plainenglish.io/dockerizing-plotly-dash-5c23009fc10b

# Dica de deploy o google cloud: https://medium.com/kunder/deploying-dash-to-cloud-run-5-minutes-c026eeea46d4

#importando as bibliotecas
from dash import Dash, Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import dash_html_components as html
import plotly.express as px

import pandas as pd

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")


tabela = pd.read_csv('./data/tabelao.csv')

#escolhendo o tema
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR, dbc_css])

server = app.server

templates = 'solar'

load_figure_template(templates)

#criando um grid
app.layout = html.Div([
    dbc.Row([html.H1('Campeonato Brasileiro', style={'text-align': 'center', 'fontSize': 75})]),
    html.Br(),
    dbc.Row([
        dbc.Col([dbc.Card([
          html.H2('Seleção de Ano', className='dbc'),
          dcc.Dropdown(id='toggle-rangeslider',
                       className="dbc",
                     options=list(tabela['ano'].unique()),
                       value=2019),
          html.Br(),


          ])],className="dbc dbc-ag-grid", md=2),


        dbc.Col([dcc.Graph(id='graph')], md=5),


        dbc.Col([dcc.Graph(id='graph_2'),
                 dbc.Row([
                     dbc.Col([
                         dcc.Dropdown(id='tipo_result',
                              className="dbc",
                              options=['gols_contra_acum','gols_pro_acum', 'gols_saldo_acum', 'pontos_acum'],
                              value= 'pontos_acum')
                     ]),
                     dbc.Col([
                         dcc.Dropdown(id='lista_2',
                         multi=True,
                         className="dbc",
                         options=list(tabela['time'].unique()),
                         value='Flamengo')])
                     ])], md=5)
    ]),

    dbc.Row([
        dbc.Col([], md=2),
        dbc.Col([], md=5),
        dbc.Col([
            dcc.Graph(id='graph_3')
        ], md=5)

    ])

])

@app.callback(
    Output('graph', "figure"),
    Input('toggle-rangeslider', "value"))

def tabela_ano(ano):

  base = tabela.loc[tabela['ano'] == ano]

  fig = px.histogram(base, x='time', y='pontos', title=f'Campeonato Brasileiro de {ano}')

  fig.update_xaxes(categoryorder='total descending')

  return fig

@app.callback(
    Output('graph_2', "figure"),
    Input('lista_2', "value"),
    Input('toggle-rangeslider', "value"),
    Input('tipo_result', "value"))

def tabela_ano(time, ano, result):

  base = tabela.loc[tabela['ano'] == ano]

  base = base.loc[base['time'].isin(time)]

  if result == 'gols_saldo_acum':

    fig = go.Figure(data=[go.Candlestick(x=base['data'],
                open=base['gols_saldo_acum_ini'],
                high=base['gols_saldo_acum_max'],
                low=base['gols_saldo_acum_min'],
                close=base['gols_saldo_acum'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_traces(increasing_line_color='#b58900', decreasing_line_color='#e83e8c')


  elif result != 'gols_saldo_acum':

    fig = px.line(base, x='data', y=result, color='time', title=f'Evolução dos {result}')

  return fig

@app.callback(
    Output('graph_3', "figure"),
    Input('toggle-rangeslider', "value"),
    Input('lista_2', "value"))

def tabela_resultado(ano, time):

  base = tabela.loc[tabela['ano'] == ano]

  base = base.loc[base['time'].isin(time)]

  fig = px.histogram(base, x='time', color='resultado', barmode='group', title=f'Resultados')

  return fig


# Run the App
if __name__ == '__main__':
    app.run(debug=True)

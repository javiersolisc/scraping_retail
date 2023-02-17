import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

data = pd.read_csv("data_dash_re.csv", sep=';')
grouped = data.groupby("phone")["brand"].count()
sorted_grouped = grouped.sort_values(ascending=False)
top_10 = sorted_grouped[:10]
data_grouped_1 = data.groupby(['brand', 'retail']).count().reset_index()
data_grouped_2 = data.groupby('brand').count().reset_index()
data_grouped_3 = data.groupby('retail').count().reset_index()


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Montserrat&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server= app.server
app.title = "MyPhone: Lo mejor para ti"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📱", className="header-emoji"),
                html.H1(
                    children="My Phone", className="header-title"
                ),
                html.P(
                    children= "Podrás ver el celular que tanto"
                    " buscabas y comparar los precios para que puedas"
                    " encontrar el que mejor se acomode a tu bolsillo",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Marca", className="menu-title"),
                        dcc.Dropdown(
                            id="marca_filtro",
                            options=[{"label": brand, "value": brand}for brand in sorted(data['brand'].unique())
                            ],
                            value="Apple",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Modelo", className="menu-title"),
                        dcc.Dropdown(
                            id="modelo_filtro",
                            options=[{"label": phone, "value": phone}for phone in data['phone'].unique()
                            ],
                            value="galaxy a03 core",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Tienda",
                            className="menu-title"
                        ),
                        dcc.Dropdown(
                            id="tienda_filtro",
                            options=[
                                {"label": retail, "value": retail} for retail in data['retail'].unique()
                            ],
                            value="ripley",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            dcc.Graph(id='barchart'),
            className='card'
        ),
        html.Div(
            dcc.Graph(
                id='hist_chart',
                figure = {
                    'data': [
                        go.Bar(
                            x=top_10.index,
                            y=top_10.values,
                            marker=dict(color='#5C8D89')
                        )
                    ],
                    'layout': go.Layout(
                        title='Top 10 modelos más ofertados',
                        xaxis={'title':'Modelos'},
                        yaxis={'title':'Cantidad de equipos'}
                    )
                }
            ),
            className='card'
        ),
        html.Div([         
            dcc.Graph(
                id='pie_chart_1',
                figure = {
                    'data': [
                        go.Pie(
                            values=data_grouped_1['phone'],
                            labels=data_grouped_1['retail'],
                            marker=dict(colors=[ '#C8E4DA','#5C8D89', '#384847','#0F887E']),
                            textposition='inside'
                        )
                    ],
                    'layout': go.Layout(
                        title='Porcentaje de celulares ofrecidos por tienda'
                    )
                },
                style={'width':'48%', 'display':'inline-block'}
            ),
            dcc.Graph(
                id='bar_chart_1',
                figure= {
                    'data': [
                        go.Bar(
                            x=data_grouped_3['retail'],
                            y=data_grouped_3['brand'],
                            marker={'color':'#5C8D89'}
                        )
                    ],
                    'layout': go.Layout(
                        title='Cantidad de equipos ofrecidos por tienda',
                        xaxis={'title':'Tienda'},
                        yaxis={'title':'Cantidad de equipos'}
                    )
                },
                style={'width':'48%', 'display':'inline-block'}
            )],
            className='card'
        ),
        html.Div(
            dcc.Graph(
            id='bar_chart_2',
            figure={
                'data':[
                    go.Bar(
                        x=data_grouped_2['brand'],
                        y=data_grouped_2['phone'],
                        marker={'color':'#5C8D89'}
                    )
                ],
                'layout': go.Layout(
                    title='Cantidad de equipos por marca',
                    xaxis={'title':'Marca'},
                    yaxis={'title': 'Número de modelos'}
                )
            } 
            ),
            className='card'
        ),
        html.Div(
            [
                html.P("© Copyright 2023, Metakuna Analytics"),
                html.P("Todos los derechos reservados.")
            ],
            className='footer'
        )
    ],
)

@app.callback(
    Output('modelo_filtro','options'),
    [Input('marca_filtro', 'value')]
)

def update_phones(brand_value):
    data_filtered = data[data['brand'] == brand_value]
    return [{'label': i, 'value':i}for i in np.sort(data_filtered['phone'].unique())]

@app.callback(
    Output('barchart','figure'),
    [
        Input('marca_filtro','value'),
        Input('modelo_filtro','value'),
        Input('tienda_filtro','value')
    ]
)

def update_figure(marca_value,modelo_value,tienda_value):
    filtered_data = data[
        (data['brand']==marca_value) &
        (data['phone']==modelo_value) &
        (data['retail']==tienda_value)
    ]

    fig = px.scatter(
        filtered_data, 
        x='price_norm', 
        y='retail', 
        color='phone',
        size='price_norm',
        labels={'phone':'Equipo','price_norm':'Precio','retail':'Tienda'}, 
        title='Busca tu equipo y mira los precios',
        color_discrete_sequence=['#5C8D89']
    )

    fig.update_layout(
        title={
            'text': 'Busca tu equipo y mira los precios',
            'font': {'size': 20},
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Precios",
        yaxis_title="Tienda",
        font=dict(
        size=15,
        color="#7f7f7f"
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
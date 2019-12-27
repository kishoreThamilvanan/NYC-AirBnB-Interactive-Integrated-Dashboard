import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

sd = pd.read_csv("cleaned_dat_500.csv")
external_stylesheets = [
    'https://codepen.io/amyoshino/pen/jzXypZ.css',
]
# print(sd)
app = dash.Dash(__name__)


app.layout = html.Div(children = [

    html.H1("NYC AirBnB Data Visualization", style={"textAlign": "center"}),

    html.Div(children = [
        html.Div(children = [
            dcc.Checklist(
                id ='check_list',
                options=[
                    {'label': i+"               ", 'value': i} for i in sd.neighbourhood_group.unique()
                ],
                value=sd.neighbourhood_group.unique(),
                className = "checklist",
            ),
        ], style = {'margin-top': 1, 'size': 10}),

        html.Div(children = [
            dcc.Graph(
                id='graph11',
            )
        ], className = 'one-half column', style={'display': 'inline-block'}),

        html.Div(children = [
            dcc.Graph(
                id='graph12',
            )
        ], className = 'one-half column', style={'align': 'right', 'display': 'inline-block'}),

    ], className = 'container'),

    html.Div(children = [

        html.Div(children = [
                dcc.Graph(
                    id='graph21',
                )
            ], className = 'one-half column'),

            html.Div(children = [
                dcc.Graph(
                    id='graph22',
                )

            ], className = 'one-half column'),

        ], className = 'container'),

],style={'textAlign':'center'})

@app.callback(
[Output('graph11', 'figure'),
Output('graph12', 'figure'),
Output('graph21', 'figure'),
Output('graph22', 'figure')],
[Input('check_list', 'value')])
def update_dashboard(boroughs):

#  for the scatter plot #1
    list=[]
    price=[]
    x=[]
    y=[]
    for i in boroughs:
        list.append(sd.reviews_per_month[sd.neighbourhood_group == i])
        price.append(sd.price[sd.neighbourhood_group == i])

    for j in list:
        for k in j:
            x.append(k)

    for j in price:
        for k in j:
            y.append(k)

    trace=[]
    for i in range(len(boroughs)):
        trace.append(go.Scatter(
            x = list[i],
            y = price[i],
            mode = 'markers',
            name = boroughs[i],
            marker={
                'size': 7,
                'opacity': 0.7,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

    figure11 = {
        'data':trace,
        'layout':go.Layout(
            title = 'Reviews per Month Vs Price',
            xaxis = {'title':'Reviews Per Month'},
            yaxis = {'title':'price'},
            hovermode = 'closest',
        )
    }

# for 2nd scatterplot
    long=[]
    lat=[]
    x=[]
    y=[]
    for i in boroughs:
        long.append(sd.longitude[sd.neighbourhood_group == i])
        lat.append(sd.latitude[sd.neighbourhood_group == i])

    for j in long:
        for k in j:
            x.append(k)

    for j in lat:
        for k in j:
            y.append(k)

    trace=[]
    for i in range(len(boroughs)):
        trace.append(go.Scatter(
            x = long[i],
            y = lat[i],
            mode = 'markers',
            name = boroughs[i],
            marker={
                'size': 7,
                'opacity': 0.7,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ))

    figure12={
        'data':trace,
        'layout':go.Layout(
            title = 'Longitude Vs Latitude',
            xaxis = {'title':'Longitude', 'fixedrange':True},
            yaxis = {'title':'Latitude', 'fixedrange':True},
            hovermode = 'closest',
        )
    }

#  for the pie chart
    list = []
    for i in boroughs:
        list.append(sd.neighbourhood_group[sd.neighbourhood_group == i].count())

    figure21 = {
            "data": [
                go.Pie(
                    labels = boroughs,
                    values = list,
                    hole= 0.4,
                    textinfo='label')],
            "layout": go.Layout(title="Neighbourhood boroughs",
                    legend={"x": 1, "y": 0.7})
    }

    # for graph 4
    # list1 = sd.neighbourhood_group[sd.room_type == 'Private room'].value_counts()
    # list2 = sd.neighbourhood_group[(sd.room_type == 'Entire home/apt')].value_counts()
    # list3 = sd.neighbourhood_group[sd.room_type == 'Shared room'].value_counts()
    # for i in boroughs:
    #     y1 = list[sd.neighbourhood_group.unique() == i]
    #     y2 = list[sd.neighbourhood_group.unique() == i]
    #     y3 = list[sd.neighbourhood_group.unique() == i]
    #

    figure22={
        "data":[
            {'x':boroughs,
             'y':sd.neighbourhood_group[sd.room_type == 'Private room'].value_counts(),
             'name':"Private Room",
             'type':'bar'},

            {'x':boroughs,
             'y':sd.neighbourhood_group[(sd.room_type == 'Entire home/apt')].value_counts(),
             'name':'Entire home/apt',
             'type':'bar'},

            {'x':boroughs,
             'y':sd.neighbourhood_group[sd.room_type == 'Shared room'].value_counts(),
             'name':'Shared room',
             'type':'bar'},
        ],

        "layout": go.Layout(title="Neighbourhood boroughs #2",)
    }

    return [figure11, figure12, figure21, figure22]

if __name__ == '__main__':
    app.run_server(port = 2023, debug = True)

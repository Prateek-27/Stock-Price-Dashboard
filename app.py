import dash
from dash import dcc
from dash import html
from datetime import date
from dash.dependencies import Input, Output, State
import pandas as pd
import pandas_datareader.data as web
import plotly.graph_objs as go
import datetime as dt

app = dash.Dash()

comp_df = pd.read_csv('NASDAQcompanylist.csv')

ticker_lst = comp_df['Symbol']
comp_lst = comp_df['Name']

start = dt.datetime(2010, 1, 29)
end = dt.datetime.today()
df = web.DataReader('AAP', 'stooq', start, end)

tick_comp_lst = [ticker_lst[x] + " " + comp_lst[x] for x in range(len(comp_df))]

app.layout = html.Div([
    html.H1("Stock Dashboard"),
    html.H3("Enter Stock Name: "),
    dcc.Dropdown(
        ticker_lst,
        ['AAP'],
        multi=True,
                id = 'selected-company'
                ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2019, 9, 10),
        max_date_allowed=dt.datetime.today(),
        initial_visible_month=date(2019, 9, 10),
        end_date=dt.datetime.today()
    ),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize':28}
    ),

    dcc.Graph(id = 'final-graph',
              figure = {'data':[go.Scatter(
                x= df.index,
                y= df['Close'],
                text='AAP',
                mode='lines',
            )],
               'layout':go.Layout(
                title = 'Stock Graph',
                hovermode='closest'
            )
             })

])
@app.callback(
    Output('final-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('selected-company', 'value'),
     State('my-date-picker-range', 'start_date'),
     State('my-date-picker-range', 'end_date')])

def update_graph(n_clicks, value, start_date, end_date):
   
    start = dt.datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.datetime.strptime(end_date[:10], '%Y-%m-%d')

    data = []
    for val in value:

        df = web.DataReader(val, 'stooq', start=start, end=end)
        trace = go.Scatter(
                x= df.index,
                y= df['Close'],
                text=val,
                mode='lines',
                name = val
            )
        data.append(trace)
        
    fig =  {
            'data': data,
            'layout': go.Layout(
                title = 'Stock Graph'
            )
        }
    return fig

from datetime import datetime
datetime.strptime('2019-09-28'[:10], '%Y-%m-%d')

if __name__ == '__main__':
    app.run_server()


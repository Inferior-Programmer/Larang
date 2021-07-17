import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import time
import plotly.graph_objs as go
import plotly.express as px

#Delete For Final uploading of code

app = dash.Dash('Item Management')

filter_List = ['Small', 'Medium', 'Large']

dataBase = np.array([{'Key 1': 'This key is for item key 1 of the small category', 'Key 2':'This key is for item key 2 of the small category' },{'Key 1': 'This key is for item key 1 of the medium category', 'Key 2':'This key is for item key 2 of the medium category' } ,{'Key 1': 'This key is for item key 1 of the large category', 'Key 2':'This key is for item key 2 of the large category' }])

def search_func(search_key, filters):
    try:
        return dataBase[filters][search_key]
    except:
        return ""

app.layout = html.Div([
    html.Div([
        html.H2('Search For Specific Item'),
        dcc.Input(id ='search', value = '', type ='text'),
        html.H2('Filters'),
        dcc.Dropdown(id ='Filters',
        options = [{'label': filter_List[i], 'value': i}
        for i in range(len(filter_List))]),
    ]),
    html.Button('search', id='submit-val', n_clicks=0),

    html.Div([], id = 'results'),

],id = 'main_class',
className ="container")

@app.callback(dash.dependencies.Output('results','children'),
    [
    dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('Filters','value'),
    dash.dependencies.State('search', 'value'),],
    )
def search_filter(n_clicks,filter_values, search_text):
    if (n_clicks == 0):
        return html.H1("")
    return html.H1(search_func(search_text, filter_values))



if __name__ == '__main__':
    app.run_server(debug=True)

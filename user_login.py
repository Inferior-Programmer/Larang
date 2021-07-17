import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import time
import plotly.graph_objs as go
import plotly.express as px
from UserDatabase import userDatabase

#Delete For Final uploading of code


app = dash.Dash('User Login')

dataBase = userDatabase()


login = [html.H1('Login'),
        html.H2('Username'),
        dcc.Input(id ='login_name', value = '', type = 'text'),
        html.H2('Password'),
        dcc.Input(id = 'password',value = '', type = 'password'),
        html.Br(),
        html.Button('Login', id = 'login_button', n_clicks=0)]

dataBase.add_user("jeremy", "lols")
app.layout = html.Div([
    html.Div([

        ], id = 'main_page'),
], id = 'Main App', className = 'container')

@app.callback(dash.dependencies.Output('main_page', 'children'),
[dash.dependencies.Input('login_button', 'n_clicks')],
[dash.dependencies.State('login_name', 'value'),
dash.dependencies.State('password','value')])
def login_userName(n_clicks, username, password):
    if(n_clicks > 0):
        if(dataBase.login(username,password)):
            return html.H1("Lols")
        return html.H2("")
    return login

if __name__ == '__main__':
    app.run_server(debug= True)

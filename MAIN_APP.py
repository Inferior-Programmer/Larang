import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import time
import plotly.graph_objs as go
import plotly.express as px
from UserDatabase import userDatabase
from ItemDataBase import itemDatabase

app = dash.Dash('User Login')


filter_List = ['None','Vegetable','Fruit','Grain']
listPostalCodeBarangay=['1116 San Bartolome','1116 Sauyo','1117 Gulod','1117 Santa Lucia','1116 Sauyo']


dataBase = userDatabase()
itemDataBase = itemDatabase()



def search_func(search_key, filters):
    try:
        initial_data = itemDataBase.search_item(search_key, 0)
        if filters == "None":
            return initial_data
        else:
            filtered_array = []
            for i in range(len(initial_data)):
                if(initial_data[i][1] == filters):
                    print(initial_data[i])
                    filtered_array.append(initial_data[i])
            return filtered_array
    except:
        return ""

login = [
        dcc.Interval(id = 'update_json', interval = 1000, n_intervals = 0),
        html.H1('Login'),
        html.H2('Username'),
        dcc.Input(id ='login_name', value = '', type = 'text'),
        html.H2('Password'),
        dcc.Input(id = 'password',value = '', type = 'password'),
        html.Br(),
        html.A(html.Button('Login', id = 'login_button', n_clicks=0),href='/user_page'),
        ]


userDashBoard = [
    html.H2('Search For Specific Item'),
    dcc.Input(id ='search', value = '', type ='text'),
    html.H2('Filters'),
    dcc.Dropdown(id ='Filters',
    options = [{'label': filter_List[i], 'value': i}
    for i in range(len(filter_List))], value = filter_List[0]),
    html.Button('search', id='submit-val', n_clicks=0),
    html.Div([], id = 'results'),
    html.A(html.Button('Logout', id = 'logout_button', n_clicks = 0), href = '/logout')]


sellerDashBoard = [
    dcc.Link(html.Button('Add New Items', id = 'addItems'), href='/addItems'),
    dcc.Link(html.Button('Add Item Stocks', id ='addInventory'), href = '/addInventory'),
    html.Div(id = 'listOfItems'),
    html.A(html.Button('Logout', id = 'logout_button', n_clicks = 0), href = '/logout')
]

register =  [html.H1('Register'),
        html.H2('Username'),
        dcc.Input(id ='register_name', value = '', type = 'text'),
        html.H2('Password'),
        dcc.Input(id = 'register_password',value = '', type = 'password'),
        html.Br(),
        html.H2("Location"),
        dcc.Dropdown(id ='locationDropdown',
        options = [{'label': listPostalCodeBarangay[i], 'value': listPostalCodeBarangay[i]}
        for i in range(len(listPostalCodeBarangay))], multi = False, value = listPostalCodeBarangay[0]),
        dcc.Checklist(id = 'sellerBool', options = [{'label': 'Seller','value':'Seller'}]),
        html.Br(),
        html.A(html.Button('Register', id = 'register_button', n_clicks=0), href ='/'),
        ]

firstPage = [
    dcc.Link(html.Button('Login'), href='/login'),
    dcc.Link(html.Button('Register'), href='/register')
]

addItemForm = [
    html.H1(id = 'add_error_message'),
    html.Br(),
    html.H1("Item Name:"),
    dcc.Input(id = 'itemName', value = '', type = 'text'),
    html.Br(),
    html.H1("Categories"),
    dcc.Dropdown(id ='Filters',
    options = [{'label': filter_List[i], 'value': i}
    for i in range(1,len(filter_List))], value = 0),
    html.Br(),
    html.H1("Price:"),
    dcc.Input(id = 'priceOfItem', value = 0, type = 'number'),
    html.Br(),
    html.H1("Stock:"),
    dcc.Input(id = 'stockOfItem', value = 0, type = 'number'),
    html.Br(),
    html.H1("Item Description"),
    dcc.Textarea(id = 'itemDescription', value = ''),
    html.Br(),
    html.Button('Add Item', id = 'add_item_button', n_clicks =0)
]






dataBase.add_user("jeremy", "lols", True, "Pogi Lols")
app.layout = html.Div([
    dcc.Store(id='session', storage_type='session'),
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'main_page'),
], id = 'Main App', className = 'container')


@app.callback(
dash.dependencies.Output('session','data'),
[dash.dependencies.Input('login_button', 'n_clicks'),
dash.dependencies.Input('update_json', 'n_intervals')],
[dash.dependencies.State('login_name', 'value'),
dash.dependencies.State('password','value')])
def login_userName(n_clicks,n_intervals, username, password):
    if(n_intervals == 0):
        return None
    if(n_clicks > 0):
        data = dataBase.login(username,password)
        if(data != None):
            print({'username': username, 'password': password,'isBuyer':data[2], 'userIndex':data[4]})
            return {'username': username, 'password': password,'isBuyer':data[2], 'userIndex':data[4], 'userInfo': data[3]}
        return None
    return None

@app.callback(dash.dependencies.Output('results','children'),
    [
    dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('Filters','value'),
    dash.dependencies.State('search', 'value'),],
    prevent_initial_call=True
    )
def search_filter(n_clicks,filter_values, search_text):
    if (n_clicks == 0):
        return html.H1("")
    results = search_func(search_text, filter_List[filter_values])

    search_results = []
    for i in range(len(results)):
        realItemName = results[i][0].split(",")
        search_results.append(html.Div([html.A(html.H1(realItemName[1]), href = '/item_page'+results[i][0]),
        html.H2("Item Category: " + results[i][1]),
        html.H3("Item Price: " + results[i][2]),
        html.H3("Stocks: " + str(results[i][3])),
        html.H3("Description: " + results[i][4]),
        ]))
    return search_results


@app.callback(dash.dependencies.Output('main_page','children'),
[dash.dependencies.Input('url','pathname'),
],
[dash.dependencies.State('session','data')])
def change_page(url, data):
    if(data != None):
        if(url == '/logout'):
            return login
        else:
            if(data['isBuyer']):
                testIfItem = url[:len("/item_page")]
                if(testIfItem == "/item_page"):
                    itemName = url[len("/item_page"):]
                    itemData = itemDataBase.search_item(itemName, 0)
                    if(itemData != None):
                        mainItem = itemData[0]
                        realItemName = mainItem[0].split(",")
                        toReturn = html.Div([html.H1(realItemName[1]),
                        html.H2("Item Category: " + mainItem[1]),
                        html.H3("Item Price: " + mainItem[2]),
                        html.H3("Stocks: " + str(mainItem[3])),
                        html.H3("Description: " + mainItem[4]),
                        html.Div(dcc.Input(id = 'hiddenInput',value = mainItem[0], disabled = True), style ={'display': 'none'}),
                        html.A(html.Button('BUY ITEM', id = 'buyItem', n_clicks = 0), href = '/')
                        ])
                        return toReturn
                return userDashBoard
            else:
                if(url == '/addItems'):
                    return addItemForm
                elif(url == '/addInventory'):
                    items = itemDataBase.search_item_user(data['username'])
                    dropDownItem = dcc.Dropdown(id = 'dropDownItem', options=[{'label': i[0] + ' - ' + str(i[3]) , 'value': i[0]} for i in items],
                    value = items[0][0])
                    return html.Div([dropDownItem, html.Br() ,dcc.Input(id = 'numberOfItemsToAdd', value = 0, type = 'number'), html.Br(),
                    html.A(html.Button('Add To Inventory', id='add_to_inventory', n_clicks = 0), href = '/addInventory')])

                return sellerDashBoard
    else:
        if(url == '/login'):
            return login
        elif(url == '/register'):
            return register
        elif(url == '/user_page'):
            return login
        else:
            return firstPage


@app.callback(dash.dependencies.Output('register_name', 'value'),
[dash.dependencies.Input('register_button','n_clicks')],
[dash.dependencies.State('register_name','value'),
dash.dependencies.State('register_password', 'value'),
dash.dependencies.State('sellerBool', "value"),
dash.dependencies.State('locationDropdown', 'value')],
prevent_initial_call=True)
def registerUser(n_clicks,name,password,value,location):
    print([name,password])
    userBool = True
    if(value):
        userBool = False
    dataBase.add_user(name, password, userBool,location)
    return name

@app.callback(dash.dependencies.Output('add_error_message', 'children'),
[dash.dependencies.Input('add_item_button','n_clicks')],
[dash.dependencies.State('itemName','value'),
dash.dependencies.State('Filters', 'value'),
dash.dependencies.State('priceOfItem','value'),
dash.dependencies.State('itemDescription', 'value'),
dash.dependencies.State('session', 'data'),
dash.dependencies.State('stockOfItem', 'value')
],
prevent_initial_call=True)
def add_items(n_clicks,itemName,filters,priceOfItem, itemDescription, userData, stockOfItem):
    errors = 0
    error_statement = ""
    if(itemName == ""):
        errors+=1
        error_statement += "\nInvalid item name"
    print(type(priceOfItem))
    if(priceOfItem <= 0):
        errors+=1
        error_statement += "\nInvalid Item Price name"
    if(itemDescription == ""):
        errors+=1
        error_statement += "\nInvalid Item Description"
    if(stockOfItem <= 0):
        errors+=1
        error_statement += "\nInvalid Item Stocks"
    if(errors>0):
        return error_statement
    if(itemDataBase.add_item(userData['username'] + ","+itemName, filter_List[filters], priceOfItem,stockOfItem, itemDescription, userData['userInfo'])):
        return html.H1("SUCCESSFULLY ADDED ITEM")
    return html.H1("ADDING ITEM UNSUCCESSFUL")



@app.callback(dash.dependencies.Output('numberOfItemsToAdd', 'value'),
[dash.dependencies.Input('add_to_inventory', 'n_clicks')],[
dash.dependencies.State('dropDownItem', 'value'),
dash.dependencies.State('numberOfItemsToAdd', 'value')
])
def add_items_toInventory(n_clicks,  selectedItem, value):
    itemData = itemDataBase.search_item(selectedItem, 0)

    itemDataBase.edit_data(selectedItem, "itemStock", itemData[0][3]+value)
    return value

@app.callback(dash.dependencies.Output('hiddenInput', 'value'),
              [dash.dependencies.Input('buyItem', 'n_clicks')],
              [dash.dependencies.State('hiddenInput', 'value')])
def decrease_item(n_clicks, itemName):
    data = itemDataBase.search_item(itemName, 0)
    realData = data[0]
    stocks = realData[3]
    itemDataBase.edit_data(itemName,3, stocks-1)
    return value

if __name__ == '__main__':
    app.run_server(debug= True)

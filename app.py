# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import pyodbc

def connectSQLServer(driver, server, db):
    #connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    connSQLServer = pyodbc.connect(
        r'DRIVER={' + driver + '};'
        r'SERVER=' + server + ';'
        r'DATABASE=' + db + ';'
        r'Trusted_Connection=yes;',
       autocommit=True
    )
    return connSQLServer

cSQL =  "SELECT "
cSQL += "   SUBSTRING(E1_EMISSAO, 7, 2) + '/' + SUBSTRING(E1_EMISSAO, 5, 2) + '/' + SUBSTRING(E1_EMISSAO, 1, 4) AS EMISSAO, "
cSQL += "   E1_NATUREZ AS NATUREZA, "
cSQL += "   ROUND(SUM(E1_VALOR),2) AS VALOR "
cSQL += "FROM SE1990 "
cSQL += "GROUP BY E1_EMISSAO, E1_NATUREZ "

# Incorporate data
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_sql_query(cSQL, connectSQLServer('SQL Server Native Client 11.0', 'DESKTOP-M3OPBE4', 'P12LG'))

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1(children='Dashboard Contas a Receber por Natureza'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='NATUREZA', y='VALOR', histfunc='sum', title='Soma por Natureza')),
    dcc.Graph(figure=px.pie(df, values='VALOR', names='NATUREZA', title='Gráfico por Natureza'))
])



def query(sqlcommand):
    sql_conn = connectSQLServer('SQL Server Native Client 11.0', 
                            'DESKTOP-AAA9999', 'P12LG') 
    cursor = sql_conn.cursor()
    cursor.execute(sqlcommand)
    rows = cursor.fetchall()
    return rows

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

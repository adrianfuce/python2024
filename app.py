#PARA GITHUB
#Dashboard financiero

#tpdps los import de paqeuetes
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc


#iniciar el dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#agregar linea de server para git:
server=app.server

app.title="Dashboard Financiero"

#data a usar:
#para que sirva en git tiene qeu estar 
df=pd.read_csv("empresas.csv")

#armar lista de las variables a usar

sales_list = ["Total Revenues", "Cost of Revenues", "Gross Profit", "Total Operating Expenses",
             "Operating Income", "Net Income", "Shares Outstanding", "Close Stock Price",
             "Market Cap", "Multiple of Revenue"]

#app layout

app.layout = html.Div([

    #html de fila con dropdowns
    html.Div([html.Div([
        #html del primer dropdown para elegir las empresas que quiero ver en el dashboard
        html.Div(dcc.Dropdown(
            id="stockdropdown", value =["Amazon", "Tesla", "Microsoft", "Apple", "Google"],clearable=False, multi=True,
            options=[{"label":x, "value":x} for x in sorted(df.Company.unique())]),
            className="six columns", style={"width":"50%"}),
        #html del segundo dropdwon para eleig que variable numerica financiera quier ver en el desahboard:
        html.Div(dcc.Dropdown(
            id="numericdropdown", value="Total Revenues", clearable=False,
            options=[{"label":x, "value":x} for x in sales_list]), className="six columns",
            style={"width":"50%"})
    #este cierra la fila y lleva classnmae row:
    ], className="row"), ], className="custom-dropdown"),

    #Html de las graficas
    html.Div([dcc.Graph(id="bar", figure={})]),

    html.Div([dcc.Graph(id="boxplot", figure={})]),

    html.Div(html.Div(id="table-container_1"), style={"marginBottom":"15px", "marginTop":"0px"}),
])

#callback para actualizar la gráfica y la tabla
@app.callback(
    #Output con todo lo que devuelve el app: las 2 graficas actualziadas en modo figure y la tabla:
    [Output("bar","figure"), Output("boxplot", "figure"), Output("table-container_1", "children")],
    [Input("stockdropdown", "value"), Input("numericdropdown", "value")]
    
)

#definición par armar las graficas y la tabla:
#esto solo se hace por como viene este dataset, no se hace siempre
def display_value(selected_stock, selected_numeric):
    if len(selected_stock)==0:
        dfv_fltrd=df[df["Company"].isin(["Amazon", "Tesla", "Microsoft", "Apple", "Google"])]
    else:
        dfv_fltrd=df[df["Company"].isin(selected_stock)]

    #haer la primera gráfica de lineas
    fig=px.line(dfv_fltrd, color="Company", x="Quarter", markers=True, y=selected_numeric,
               width=1000, height=500)
    #hacer titulo de la grafica variable:
    fig.update_layout(title=f"{selected_numeric} de {selected_stock}",
                     xaxis_title="Quarters")

    fig.update_traces(line=dict(width=2))

#grafica de boxplot
    fig2=px.box(dfv_fltrd, color="Company", x="Company", y=selected_numeric, width=1000, height=500)

    fig2.update_layout(title=f"{selected_numeric} de {selected_stock}")

    #modificar el dataframe para poder hacerlo una tabla 
    df_reshaped = dfv_fltrd.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()

#forma en que se despliegta la tabla
    return (fig, fig2,
          dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped2.columns],
                              data=df_reshaped2.to_dict("records"),
                              export_format="csv", #para guardar en csv la tabla
                              fill_width=True,
                              style_cell={"font-size":"12px"},
                              style_table={"maxWidth":1000},
                              style_header={"backgroundColor":"blue",
                                           "color":"white"},
                              style_data_conditional= [{"backgroundColor":"white",
                                                     "color":"black"},
                            ]))

#set server y correr el app

#para GITHUB agregar el host y debug
if __name__=="__main__":
    app.run_server(debug=False, host="0.0.0.0",port=10000)
    

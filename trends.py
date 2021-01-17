import os
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, time, date, timedelta
import csv
import requests
from io import StringIO
import boto3

#https://www.inegi.org.mx/servicios/api_indicadores.html#introduccion
inegi_state = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", 
               "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", 
               "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
               "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
               "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", 
               "Zacatecas"]

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID']
#for local test please uncomment the following lines
#aws_access_key_id = ""
#aws_secret_access_key = ""
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def plot_trends(content_type):
    if content_type == "region":
        #very important to include the parameters: Bucket and Key
        csv_obj = s3.get_object(Bucket="open-hr-google-trends", Key = "region.csv")
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        region = pd.read_csv(StringIO(csv_string))
        region_last = region[region.date >= region.date.max()]
        states = region_last.geoname.tolist()
        values = region_last.bolsa_de_trabajo.tolist()
        bar_region = [go.Bar(x=states, y = values, marker_color='rgb(10, 24, 69)')]
        layout_region = dict(title=dict(text='"Bolsa de Trabajo" by state in Mexico',
                                        font=dict(size=20,color='#0a1845')),
                             xaxis = dict(title = 'State',),
                             yaxis = dict(title = 'Search value'),)
        region_plot = [dict(data=bar_region, layout=layout_region)]
        return(region_plot)
    elif content_type == "historical":
        csv_obj = s3.get_object(Bucket="open-hr-google-trends", Key = "historical.csv")
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        historical = pd.read_csv(StringIO(csv_string))
        #historical = pd.read_csv("historical.csv")
        dates = historical.date.tolist()
        values = historical["bolsa de trabajo"].tolist()
        over_time = [go.Scatter(x=dates, y = values, marker_color='rgb(10, 24, 69)')]
        layout_historical = dict(title=dict(text='"Bolsa de Trabajo" a través del tiempo',
                                        font=dict(size=20,color='#0a1845')),
                             xaxis = dict(title = 'Fechas',),
                             yaxis = dict(title = 'Valor de la búsqueda'),)
        historical_plot = [dict(data=over_time, layout=layout_historical)]
        return(historical_plot)

def plot_inegi(content_type):
    pos = content_type.find("-")
    path = content_type[:pos]
    content_type = content_type[pos+1:]
    csv_obj = s3.get_object(Bucket="open-hr-google-trends", Key = path + ".csv")
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    #df = pd.read_csv(path + ".csv")
    if content_type == "gender":
        states = df.states.to_list()
        males = df.male.to_list()
        females = df.female.to_list()
        per_males = df.per_males.to_list()
        per_females = df.per_females.to_list()
        bar_gender_male = go.Bar(name = "Hombres", x = states, y = males, marker = {"color":'#0a1845'})
        bar_gender_female = go.Bar(name = "Mujeres", x = states, y = females, marker = {"color": "#FFB6C1"})
        bar_gender_male_per = go.Bar(name = "% Hombres", x = states, y = per_males, marker = {"color":'#0a1845'}, visible = False)
        bar_gender_female_per = go.Bar(name = "% Mujeres", x = states, y = per_females, marker = {"color": "#FFB6C1"}, visible= False)
        data = [bar_gender_male, bar_gender_female, bar_gender_male_per, bar_gender_female_per]
        updatemenus = list([
                            dict(active=0,
                                showactive = True,
                                buttons=list([   
                                            dict(label = "Total",
                                                method = "update",
                                                args = [{"visible": [True, True, False, False]}]),
                                            dict(label = "Porcentage",
                                                method = "update",
                                                args = [{"visible": [False, False, True, True]}])]))])
        layout_gender = dict(title=dict(text = "Female and male by state",
                                        font=dict(size = 20, color = '#0a1845')),
                            title_x=0.5,
                            barmode = "group",
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = dict(title= "State",),
                            yaxis = dict(title = "Population", showgrid=True, gridcolor='#ececec'),
                            updatemenus=updatemenus,)
        final_plot = [dict(data=data, layout = layout_gender)]
    elif content_type == "relative":
        states = df.states.to_list()
        total = df.total.sum()
        values = df.total / total
        bar_relative = [go.Bar(x=states, y = values, marker_color='rgb(50, 91, 121)')]
        layout_relative = dict(title=dict(text='Población por estado',
                                    font=dict(size=20,color='#0a1845')),
                         xaxis = dict(title = 'State',),
                         yaxis = dict(title = 'Población relativa'),)
        final_plot = [dict(data=bar_relative, layout=layout_relative)]
    elif content_type == "age":
        states = df.states.to_list()
        final_plot = go.Figure()

        cols = ["twenties", "thirties", "fourties", "fifties", "sixties"]
        vals = ["20-29", "30-39", "40-49", "50-59", "60-69"]
        
        for age in cols:  
            values = df[age].values 
            final_plot.add_trace(
                go.Bar(x = states,
                    y = values,
                    visible = False,
                    marker_color='rgb(50, 91, 121)'))

        final_plot.data[0].visible = True

        steps = []
        for i in range(len(final_plot.data)):
            step = dict(
                method="update",
                args=[{"visible": [False] * len(final_plot.data)},
                    {"title": "Total población por edad: " + vals[i]}],
                label = vals[i])
            step["args"][0]["visible"][i] = True 
            steps.append(step)

        sliders = [dict(active=5,
                        currentvalue={"prefix": "Edades: "},
                        y = -0.5,
                        steps=steps)]

        final_plot.update_layout(
            sliders=sliders,
            plot_bgcolor='rgba(0,0,0,0)',
            title = {'text' : "Total población por edad: 20-29", "font":{"size":20, "color":'#0a1845'}, "x":0.5},
            xaxis= {"title":"Estado"},
            yaxis = {"title": "Población", "showgrid":True, "gridcolor":'#ececec'},
            height=600)
            
    elif content_type == "age_relative":
        states = df.states.to_list()
        final_plot = go.Figure()

        cols = ["per_twenties", "per_thirties", "per_fourties", "per_fifties", "per_sixties"]
        vals = ["20-29", "30-39", "40-49", "50-59", "60-69"]
        
        for age in cols:  
            values = df[age].values 
            final_plot.add_trace(
                go.Bar(x = states,
                    y = values,
                    visible = False,
                    marker_color='rgb(50, 91, 121)'))

        final_plot.data[0].visible = True

        steps = []
        for i in range(len(final_plot.data)):
            step = dict(
                method="update",
                args=[{"visible": [False] * len(final_plot.data)},
                    {"title": "Población relativa por edad: " + vals[i]}],
                label = vals[i])
            step["args"][0]["visible"][i] = True 
            steps.append(step)

        sliders = [dict(active=5,
                        currentvalue={"prefix": "Edades: "},
                        y = -0.5,
                        steps=steps)]

        final_plot.update_layout(
            sliders=sliders,
            plot_bgcolor='rgba(0,0,0,0)',
            title = {'text' : "Población relativa por edad: 20-29", "font":{"size":20, "color":'#0a1845'}, "x":0.5},
            xaxis= {"title":"Estado"},
            yaxis = {"title": "Población relativa", "showgrid":True, "gridcolor":'#ececec'},
            height=600)
    
    elif content_type == "unemployment_rate":
        csv_obj = s3.get_object(Bucket="open-hr-google-trends", Key = "historical.csv")
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        historical = pd.read_csv(StringIO(csv_string))
        #historical = pd.read_csv("historical.csv")
        min_date = historical.date.min()
        df = df[df.time >= min_date]
        dates = df.time.tolist()
        values = df["unemployment_rate"].tolist()
        over_time = [go.Scatter(x=dates, y = values, marker_color='rgb(50, 91, 121)')]
        layout_historical = dict(title=dict(text='Unemployment rate',
                                        font=dict(size=20,color='#0a1845')),
                             xaxis = dict(title = 'Dates',),
                             yaxis = dict(title = 'Unemployment rate'),)
        final_plot = [dict(data=over_time, layout=layout_historical)]
    
    return(final_plot)

def main():
    plot_region = plot_trends(content_type="region")[0]
    plot_population = plot_inegi("population-relative")[0]
    _plot_gender = plot_inegi("population-gender")[0]
    plot_historical = plot_trends(content_type="historical")[0]
    _plot_age = plot_inegi("population-age")
    _plot_age_relative = plot_inegi("population-age_relative")
    plot_unemployment = plot_inegi(content_type="employment-unemployment_rate")[0]
    return([plot_historical, plot_unemployment, plot_region, plot_population, _plot_age, _plot_age_relative, _plot_gender])

if __name__ == "__main__":
    main()



import os
from pytrends.request import TrendReq
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, time, date, timedelta
import csv
import requests

#https://www.inegi.org.mx/servicios/api_indicadores.html#introduccion
inegi_state = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", 
               "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", 
               "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
               "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
               "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", 
               "Zacatecas"]

#https://github.com/GeneralMills/pytrends
def download_trends(content_type):
    #from mexico
    pytrends = TrendReq(hl='es-MX', tz=360)
    kw_list = ["bolsa de trabajo"]
    if content_type == "historical":
        #last seven days
        pytrends.build_payload(kw_list, timeframe='now 7-d', geo='MX', gprop='')
        #this returns pandas dataframe
        historical = pytrends.interest_over_time()
        bolsa_trabajo_value = int(historical.resample("W").mean()[0])
        append_csv([str(date.today())] + [bolsa_trabajo_value],"historical.csv")
    elif content_type == "region":
        #which state is searching more 
        regions = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
        regions.reset_index(inplace=True)
        region_list = regions.to_numpy()
        for region in region_list:
            append_csv([str(date.today())] + list(region), "region.csv")
            #We are appending csv data not writting again


def download_inegi(content_type, token):
    """
    Process data from INEGI API
    """
    data_dictionary = {}
    #there might be an easier way to extract all states info
    if content_type == "population":
        for state in range(1, 33):
            if state < 10:
                url = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002,1002000003/es/0700000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
            else:
                url = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002,1002000003/es/070000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
            response = requests.get(url)
            json_response = response.json()
            males = int(float(json_response['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE']))
            females = int(float(json_response['Series'][1]['OBSERVATIONS'][0]['OBS_VALUE']))
            total = males + females
            per_males = males / total
            per_females = females / total
            inegi_state[14] = "Estado de México"
            data_dictionary[inegi_state[state-1]] = [males, females, total, per_males, per_females]
    df = pd.DataFrame.from_dict(data_dictionary, orient='index', columns = ["male", "female", "total", "per_males", "per_females"])
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'states'})
    df.replace("México", "Estado de México")
    df.to_csv(content_type + ".csv", index = False)

def append_csv(to_append, path_to_write):
    with open(path_to_write, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(to_append)

def plot_trends(content_type):
    if content_type == "region":
        region = pd.read_csv("region.csv")
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
        historical = pd.read_csv("historical.csv")
        dates = historical.date.tolist()
        values = historical["bolsa de trabajo"].tolist()
        over_time = [go.Scatter(x=dates, y = values, marker_color='rgb(10, 24, 69)')]
        layout_historical = dict(title=dict(text='"Bolsa de Trabajo" over time',
                                        font=dict(size=20,color='#0a1845')),
                             xaxis = dict(title = 'Dates',),
                             yaxis = dict(title = 'Search value'),)
        historical_plot = [dict(data=over_time, layout=layout_historical)]
        return(historical_plot)

def plot_inegi(content_type):
    pos = content_type.find("-")
    path = content_type[:pos]
    content_type = content_type[pos+1:]
    df = pd.read_csv(path + ".csv")
    states = df.states.to_list()
    if content_type == "gender":
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
        total = df.total.sum()
        values = df.total / total
        bar_relative = [go.Bar(x=states, y = values, marker_color='rgb(50, 91, 121)')]
        layout_relative = dict(title=dict(text='Población por estado',
                                    font=dict(size=20,color='#0a1845')),
                         xaxis = dict(title = 'State',),
                         yaxis = dict(title = 'Población relativa'),)
        final_plot = [dict(data=bar_relative, layout=layout_relative)]
    return(final_plot)

def main():
    last_modification_region = datetime.fromtimestamp(os.path.getmtime("region.csv")).date()
    last_modification_historical = datetime.fromtimestamp(os.path.getmtime("historical.csv")).date()
    if (date.today() - last_modification_region).days > 7:
        download_trends(content_type="region")
    if  ((date.today() - last_modification_historical).days > 7) and (date.today().weekday() == 6):
        download_trends(content_type="historial")
    if  ((date.today() - last_modification_historical).days < 7) and (date.today().weekday() == 6):
        download_trends(content_type="historial")
    if  ((date.today() - last_modification_historical).days > 7) and (date.today().weekday() != 6):
        print("Please add necessary week")
    else:
        pass
    plot_region = plot_trends(content_type="region")[0]
    plot_population = plot_inegi("population-relative")[0]
    _plot_gender = plot_inegi("population-gender")[0]
    plot_historical = plot_trends(content_type="historical")[0]
    return([plot_historical, plot_region, plot_population, _plot_gender])

if __name__ == "__main__":
    main()



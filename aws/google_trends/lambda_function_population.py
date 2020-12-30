import json
import boto3
import os
import pandas as pd
import csv
import requests
from io import StringIO

#https://www.inegi.org.mx/servicios/api_indicadores.html#introduccion
inegi_state = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila", 
               "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato", 
               "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
               "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
               "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", 
               "Zacatecas"]

s3_resource = boto3.resource('s3')
token = os.environ['TOKEN']

def lambda_handler(event, context):
    data_dictionary = {}
    for state in range(1, 33):
        #you can make it all in one, like age example
        if state < 10:
            url_gender = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002,1002000003/es/0700000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
            url_age = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000070,1002000073,1002000076,1002000079,1002000082,1002000085,1002000091,1002000094,1002000097,1002000100/es/0700000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
        else:
            url_gender = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000002,1002000003/es/070000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
            url_age = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000070,1002000073,1002000076,1002000079,1002000082,1002000085,1002000091,1002000094,1002000097,1002000100/es/070000{state}/true/BISE/2.0/".format(state = str(state)) + token + "?type=json"
        #creatimg a function might reduce code
        response_gender = requests.get(url_gender)
        response_age = requests.get(url_age)
        json_response_gender = response_gender.json()
        json_response_age = response_age.json()["Series"]
        males = int(float(json_response_gender['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE']))
        females = int(float(json_response_gender['Series'][1]['OBSERVATIONS'][0]['OBS_VALUE']))
        total = males + females
        per_males = males / total
        per_females = females / total
        value = [males, females, total, per_males, per_females]
        for ages in range(10):
            if ages % 2==0:
                age1 = int(float(json_response_age[ages]['OBSERVATIONS'][0]['OBS_VALUE']))
                age2 = int(float(json_response_age[ages + 1]['OBSERVATIONS'][0]['OBS_VALUE']))
                value.append(age1 + age2)
                value.append((age1 + age2)/total)
        inegi_state[14] = "Estado de México"
        data_dictionary[inegi_state[state-1]] = value
    df = pd.DataFrame.from_dict(data_dictionary, orient='index', columns = ["male", "female", "total", "per_males", "per_females", "twenties", "per_twenties", "thirties", "per_thirties", "fourties", "per_fourties", "fifties", "per_fifties", "sixties", "per_sixties"])
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'states'})
    df.replace("México", "Estado de México")
    
    bucket = 'open-hr-google-trends'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource.Object(bucket, 'population.csv').put(Body=csv_buffer.getvalue())

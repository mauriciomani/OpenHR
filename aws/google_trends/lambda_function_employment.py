import json
import boto3
import os
import pandas as pd
import csv
import requests
from io import StringIO

s3_resource = boto3.resource('s3')
token = os.environ['TOKEN']

def lambda_handler(event, context):
    employment = {}
    #tasa desocupacion desestacionalizada
    url_unemployment_rate = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/444884/es/0700/false/BIE/2.0/" + token + "?type=json"
    response_unemployment_rate = requests.get(url_unemployment_rate)
    json_response_unemployment_rate = response_unemployment_rate.json()["Series"][0]["OBSERVATIONS"]
    for observation in json_response_unemployment_rate:
        employment[observation["TIME_PERIOD"]] = [float(observation["OBS_VALUE"])/100]
    #I am separating it since I got problems when joinning
    #tasa desocupacion
    url_unemployment = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/444603/es/0700/false/BIE/2.0/" + token + "?type=json"
    response_unemployment = requests.get(url_unemployment)
    json_response_unemployment = response_unemployment.json()["Series"][0]["OBSERVATIONS"]
    for observation in json_response_unemployment:
        employment[observation["TIME_PERIOD"]].append(float(observation["OBS_VALUE"])/100)
    #Tasa de subocupacion desestacionalizada
    url_subemployment_rate = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/444889/es/0700/false/BIE/2.0/" + token + "?type=json"
    response_subemployment_rate = requests.get(url_subemployment_rate)
    json_response_subemployment_rate = response_subemployment_rate.json()["Series"][0]["OBSERVATIONS"]
    for observation in json_response_subemployment_rate:
        employment[observation["TIME_PERIOD"]].append(float(observation["OBS_VALUE"])/100)
    df = pd.DataFrame.from_dict(employment, orient = "index", columns = ["unemployment_rate", "unemployment_rate_seas", "subemployment_rate"])
    df.reset_index(inplace = True)
    df = df.rename(columns = {'index':'time'})
    df["time"] = pd.to_datetime(df.time)
    
    bucket = 'open-hr-google-trends'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource.Object(bucket, 'employment.csv').put(Body=csv_buffer.getvalue())
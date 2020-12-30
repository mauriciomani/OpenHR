import json
import boto3
import os
import pandas as pd
import csv
from io import StringIO
from pytrends.request import TrendReq

s3_resource = boto3.resource('s3')

def lambda_handler(event, context):
    old_df = pd.read_csv("s3://open-hr-google-trends/historical.csv")
    pytrends = TrendReq(hl='es-MX', tz=360)
    kw_list = ["bolsa de trabajo"]
    pytrends.build_payload(kw_list, timeframe='now 7-d', geo='MX', gprop='')
    #this returns pandas dataframe
    historical = pytrends.interest_over_time()
    bolsa_trabajo_value = historical.resample("W").mean()
    bolsa_trabajo_value.reset_index(inplace = True)
    bolsa_trabajo_value['date'] = bolsa_trabajo_value['date'].dt.date
    df = old_df.append(bolsa_trabajo_value)
    
    bucket = 'open-hr-google-trends'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, 'historical.csv').put(Body=csv_buffer.getvalue())

import json
import boto3
import os
import pandas as pd
import csv
from io import StringIO
from pytrends.request import TrendReq
from datetime import datetime, time, date, timedelta

s3_resource = boto3.resource('s3')

def lambda_handler(event, context):
    old_df = pd.read_csv("s3://open-hr-google-trends/region.csv")
    pytrends = TrendReq(hl='es-MX', tz=360)
    kw_list = ["bolsa de trabajo"]
    pytrends.build_payload(kw_list, timeframe='now 7-d', geo='MX', gprop='')
    regions = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    regions.reset_index(inplace=True)
    regions["date"] = str(date.today())
    regions[["date", "geoName", "bolsa de trabajo"]]
    regions.rename(columns = {"geoName": "geoname", "bolsa de trabajo": "bolsa_de_trabajo"}, inplace = True)
    df = old_df.append(regions)
    
    bucket = 'open-hr-google-trends'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index = False)
    s3_resource.Object(bucket, 'region.csv').put(Body=csv_buffer.getvalue())

import requests
import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
import time

API_KEY = 'YKWFY2IQE15YO7OO'
symbol = 'AAPL'

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

response = requests.get(url)
data = response.json()
time_series = data["Time Series (Daily)"]


token = "yYFnlBcX4SwXBAVPwCEwSux8cj5CQ4cueXBx25U6fD2xRb4TCNzxwNqU6j2GaSqsDxM3J-m-ZvGJI3Qf8Fl-jw=="
org = "ktu"
bucket = "stock_data"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = client.write_api()


for date_str, values in time_series.items():
    date = datetime.strptime(date_str, "%Y-%m-%d")
    close_price = float(values["4. close"])

    point = Point("stock_price") \
        .tag("symbol", symbol) \
        .field("close", close_price) \
        .time(date, WritePrecision.NS)

    write_api.write(bucket=bucket, org=org, record=point)

print(" Finans verileri InfluxDB'ye yazıldı.")

time.sleep(2)


# BAŞKA FİNANS APİSİ
#  f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact'
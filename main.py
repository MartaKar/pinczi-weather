import os
from influxdb_client import InfluxDBClient
from flask import Flask, render_template

app = Flask(__name__)

os.environ[
    "INFLUXDB_TOKEN"] = "ZplOmxakWYZe8BnDXxLqrvPBcWvkyZTCWauPcBW8LVZ48i2M7wTHAwgPqW0wGm7LbISlTJdNayex70mWzZNw4g=="

token = os.environ.get("INFLUXDB_TOKEN")

org = "pkaras3@gmail.com"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

with InfluxDBClient(url=url, token=token, org=org) as client:
    query_api = client.query_api()
    query_temp = """from(bucket: "home_assistant")
    |> range(start: -10m)
    |> filter(fn: (r) => r["_measurement"] == "°C")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["domain"] == "sensor")
    |> filter(fn: (r) => r["entity_id"] == "pws_temperature")
    |> filter(fn: (r) => r["friendly_name"] == "PWS - Temperature")
    |> filter(fn: (r) => r["source"] == "HA")"""
    query_rain = """from(bucket: "home_assistant")
	|> range(start: -10m)
    |> filter(fn: (r) => r["_measurement"] == "mm/h")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["domain"] == "sensor")
    |> filter(fn: (r) => r["entity_id"] == "pws_rainrate")
    |> filter(fn: (r) => r["friendly_name"] == "PWS - Rainrate")
    |> filter(fn: (r) => r["source"] == "HA")"""
    query_wind = """from(bucket: "home_assistant")
	|> range(start: -10)
    |> filter(fn: (r) => r["_measurement"] == "m/s")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["domain"] == "sensor")
    |> filter(fn: (r) => r["entity_id"] == "pws_wind_speed")
    |> filter(fn: (r) => r["friendly_name"] == "PWS - Wind speed")
    |> filter(fn: (r) => r["source"] == "HA")"""
    query_pressure = """from(bucket: "home_assistant")
	|> range(start: -10)
    |> filter(fn: (r) => r["_measurement"] == "hPa")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["domain"] == "sensor")
    |> filter(fn: (r) => r["entity_id"] == "pws_barometer_absolute")
    |> filter(fn: (r) => r["friendly_name"] == "PWS - Barometer (absolute)")
    |> filter(fn: (r) => r["source"] == "HA")"""


    def query_value(query_name):
        tables = query_api.query(query_name)
        for table in tables:
            for record in table.records:
                output = str(record.get_value())
                return output


    temperature = query_value(query_temp)
    rain = query_value(query_rain)
    wind = query_value(query_wind)
    pressure = query_value(query_pressure)
    if rain is None:
        rain = 0




@app.route('/')
def weather():
    return render_template('index.html', temp=temperature, rain=rain, wind=wind, pressure= pressure)


if __name__ == '__main__':
    app.run()

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

    tables = query_api.query("""from(bucket: "home_assistant")
    |> range(start: -10m)
    |> filter(fn: (r) => r["_measurement"] == "°C")
    |> filter(fn: (r) => r["_field"] == "value")
    |> filter(fn: (r) => r["domain"] == "sensor")
    |> filter(fn: (r) => r["entity_id"] == "pws_temperature")
    |> filter(fn: (r) => r["friendly_name"] == "PWS - Temperature")
    |> filter(fn: (r) => r["source"] == "HA")""")

    for table in tables:
        for record in table.records:
            temperature = str(record.get_value())


@app.route('/')
def weather():
    return render_template('index.html', temp=temperature)

if __name__ == '__main__':
    app.run()
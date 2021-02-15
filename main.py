import os

from datetime import datetime

from fastapi import FastAPI

from pydantic import BaseModel

from aioinflux import InfluxDBClient


app = FastAPI()

influx_client = InfluxDBClient(host="influxdb", db=os.getenv('INFLUXDB_DB', ''))


class Temperature(BaseModel):
    temperature: float


class Humidity(BaseModel):
    humidity: float


@app.post("/temperature")
async def save_temperature(item: Temperature):
    await influx_client.write({
            "time": str(datetime.utcnow()),
            "measurement": "temperature",
            "fields": {"value": item.temperature}
        })
    return {"success": True}


@app.post("/humidity")
async def save_temperature(item: Humidity):
    await influx_client.write({
            "time": str(datetime.utcnow()),
            "measurement": "humidity",
            "fields": {"value": item.humidity}
        })
    return {"success": True}


@app.get("/temperature")
async def get_temperature():
    return await influx_client.query('SELECT value FROM temperature WHERE time > now() - 2h')


@app.get("/humidity")
async def get_temperature():
    return await influx_client.query('SELECT value FROM humidity WHERE time > now() - 2h')

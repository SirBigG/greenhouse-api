import os

from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from aioinflux import InfluxDBClient


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def get_temperature(period: str = '1h'):
    return await influx_client.query(f'SELECT * FROM temperature WHERE time > now() - {period}')


@app.get("/humidity")
async def get_humidity(period: str = '1h'):
    return await influx_client.query(f'SELECT * FROM humidity WHERE time > now() - {period}')

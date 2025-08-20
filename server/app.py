import os
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "my-token")
INFLUX_ORG = os.getenv("INFLUX_ORG", "my-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "system")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

app = FastAPI(title="Watcher", description="Receive system metrics and store in InfluxDB")

class VMStatus(BaseModel):
    name: str
    status: str

class Metrics(BaseModel):
    power_on: bool
    cpu_load: float
    memory_usage: float
    backhaul: str
    vms: List[VMStatus]
    temperature: float
    humidity: float
    enclosure_door: bool
    lte_active: bool

@app.post("/metrics")
async def ingest_metrics(metrics: Metrics):
    point = (
        Point("system_status")
        .tag("backhaul", metrics.backhaul)
        .field("power_on", int(metrics.power_on))
        .field("cpu_load", metrics.cpu_load)
        .field("memory_usage", metrics.memory_usage)
        .field("temperature", metrics.temperature)
        .field("humidity", metrics.humidity)
        .field("enclosure_door", int(metrics.enclosure_door))
        .field("lte_active", int(metrics.lte_active))
    )
    for vm in metrics.vms:
        point.field(f"vm_{vm.name}", 1 if vm.status == "running" else 0)
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

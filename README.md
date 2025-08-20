# Watcher Dashboard

Watcher is a web dashboard server that receives metrics from downstream nodes and presents them in Grafana with a black and red theme.

## Features
- Collects metrics such as power status, CPU load, memory usage, backhaul type, virtual machine statuses, environmental readings (temperature, humidity, door), and LTE transmission state.
- Stores metrics in InfluxDB for efficient time-series storage.
- Exposes a REST endpoint for downstream devices to send metrics via IP messages.
- Grafana dashboard styled with a militaristic black background and red highlights.

## Running with Docker

```
docker compose up --build
```

This will start:
- `app` – the FastAPI server listening on port 8000
- `influxdb` – InfluxDB instance on port 8086
- `grafana` – Grafana UI on port 3000

Grafana is pre-provisioned with the InfluxDB data source and a dashboard at `http://localhost:3000/` (default credentials `admin/secret`).

## Sending Metrics

POST metrics to `http://localhost:8000/metrics` with JSON payload:

```json
{
  "power_on": true,
  "cpu_load": 0.42,
  "memory_usage": 30.5,
  "backhaul": "satellite",
  "vms": [{"name": "router", "status": "running"}],
  "temperature": 28.4,
  "humidity": 40.2,
  "enclosure_door": false,
  "lte_active": true
}
```

## Development

Install dependencies and run the server locally:

```
pip install -r requirements.txt
uvicorn server.app:app --reload
```

Then open Grafana at [http://localhost:3000](http://localhost:3000).

## Testing

Run unit tests (none yet but command shown for consistency):

```
pytest
```

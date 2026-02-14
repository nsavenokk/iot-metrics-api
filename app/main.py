from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI(title="IoT Metrics API", version="1.0.0")


class MetricIn(BaseModel):
    device_id: str
    temperature: float


class MetricOut(MetricIn):
    ts: str


_STORAGE: List[MetricOut] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/metrics", response_model=MetricOut)
def add_metric(metric: MetricIn):
    item = MetricOut(**metric.model_dump(), ts=datetime.utcnow().isoformat() + "Z")
    _STORAGE.append(item)
    return item


@app.get("/metrics", response_model=List[MetricOut])
def list_metrics(limit: int = 10):
    return _STORAGE[-limit:]

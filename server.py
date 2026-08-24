from scanner.pipeline import run_full_scan
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ScanRequest(BaseModel):
    cities: list[str]
    premium: bool

@app.get("/profits.json")
def get_profits():
    return FileResponse("storage/profits.json")

@app.post("/scan")
def scan(req: ScanRequest):
    cities = req.cities
    premium = req.premium
    run_full_scan(cities, premium)

    return {"status": "ok"}
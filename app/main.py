# This project is a FastAPI service built on top of the pybaseball library:
# https://github.com/jldbc/pybaseball
#
# This service is not affiliated with MLB or the official data sources used by pybaseball.

from fastapi import FastAPI
from app.api.v1.schemas import router as schemas_router

app = FastAPI(title="PyBaseball API Service")

@app.get("/healthz")
def health():
    return {"status": "ok"}

app.include_router(schemas_router, prefix="/v1/schemas")
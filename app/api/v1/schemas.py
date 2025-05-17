# This project is a FastAPI service built on top of the pybaseball library:
# https://github.com/jldbc/pybaseball
#
# This service is not affiliated with MLB or the official data sources used by pybaseball.

from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.registry.datasets import DATASET_REGISTRY
from app.utils.sanitize import sanitize_dataframe
import pandas as pd

router = APIRouter()

@router.get("")
def list_schemas():
    return list(DATASET_REGISTRY.keys())

@router.get("/{source}")
def get_source_metadata(source: str):
    source_meta = DATASET_REGISTRY.get(source)
    if not source_meta:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {
        "description": source_meta.get("description", f"Tables from {source}"),
        "tables": list(source_meta.get("tables", {}).keys())
    }

@router.get("/{source}/tables")
def list_tables_in_source(source: str):
    source_meta = DATASET_REGISTRY.get(source)
    if not source_meta:
        raise HTTPException(status_code=404, detail="Data source not found")
    return list(source_meta.get("tables", {}).keys())

@router.get("/{source}/tables/{table_name}")
def get_table_schema(source: str, table_name: str):
    table = DATASET_REGISTRY.get(source, {}).get("tables", {}).get(table_name)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return {
        "description": table["description"],
        "params": table["params"]
    }

@router.get("/{source}/tables/{table_name}/data")
def query_table_data(source: str, table_name: str, request: Request):
    table = DATASET_REGISTRY.get(source, {}).get("tables", {}).get(table_name)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    fn = table["function"]
    param_names = table["params"]
    query_params = dict(request.query_params)

    args = {}
    for param in param_names:
        if param in query_params:
            args[param] = query_params[param]
        elif param in table.get("required", []):
            raise HTTPException(status_code=400, detail=f"Missing required parameter: '{param}'")

    try:
        result = fn(**args)
        if isinstance(result, pd.DataFrame):
            result = sanitize_dataframe(result)
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
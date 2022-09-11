import os
import json
import datetime as dt
from typing import Union
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .aws import aws
from .config import config_handler

app = FastAPI()
APP_NAME = "tracking_api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run(f"{APP_NAME}.main:app", host="0.0.0.0", port=8000, reload=True)


def write_json_file(filename: str, json_data: dict):
    Path(filename).open("w").write(json.dumps(json_data))
    return True

def get_timestamp() -> str:
    return str(dt.datetime.today()).split(".")[0].replace(" ", "_").replace(":", "")

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/healthcheck/")
async def create_item(item):
    print(item)
    return item

@app.get("/test-response/", tags=["Web UI"])
async def test_response():
    return "test hello world"

@app.post("/acceptdata")
async def accept_data(request: Request):
    try:
        result = await request.json()
        timestamp = get_timestamp()
        result['post_timestamp'] = timestamp
        print(result)
        object_name = f"{APP_NAME}_{timestamp}.json"
        file_path = str(Path(object_name).resolve())
        write_json_file(filename=file_path, json_data=result)
        aws.upload_json(object_name=object_name, file_path=file_path)
        return result
    except json.JSONDecodeError as e:
        print(e)
        return e
    finally:
        os.remove(file_path)

# https://vlee.kr/4632
# http://localhost:8889/docs
import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# import pymysql
from pydantic import BaseModel
from typing import List

templates = Jinja2Templates(directory="template")

app = FastAPI()
# app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse( "index_demo.html",{"request" : request, "student" : { "age" : 10, "name" : "shk" } })


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile] = File(...)):
    UPLOAD_DIRECTORY = "./download/"
    for file in files:
        contents = await file.read()
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
            fp.write(contents)
        print(file.filename)
    return {"filenames": [file.filename for file in files]}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8889 )
    # uvicorn.run(app, host="0.0.0.0", port=8889, ssl-keyfile="key.pem" ssl-certfile="cert.pem" )
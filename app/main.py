from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from tripper.datadoc import TableDoc
from tripper import Triplestore
import pandas as pd
import os
import tempfile

app = FastAPI()

templates = Jinja2Templates(directory="templates")
select_iri = "http://10.218.121.139:7200/repositories/MatCHMaker"
update_iri = "http://10.218.121.139:7200/repositories/MatCHMaker/statements"


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Main Page with file upload"""
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/uploadDocumentation/")
async def upload_Documentation(file: UploadFile = File(...)):
    """Add Documentation from an Excel sheel"""
    if not file.filename.endswith((".xls", ".xlsx", ".csv")):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an Excel file."
        )
    ts = Triplestore("sparqlwrapper", base_iri=select_iri, update_iri=update_iri)
    # td = TableDoc.parse_csv(
    #     "https://raw.githubusercontent.com/HEU-MatCHMaker/DataDocumentation/refs/heads/sem-example/examples/SEM_cement_batch2/input/datasets.csv"
    # )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        td = TableDoc.parse_csv(temp_file_path)
    finally:
        os.remove(temp_file_path)
    td.save(ts)
    return f"{file.filename} had populated the Graph"

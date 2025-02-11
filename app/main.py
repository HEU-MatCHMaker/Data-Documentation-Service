from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from tripper.datadoc import TableDoc
from tripper import Triplestore
import aiohttp
import os
import tempfile
from urllib.parse import urlparse, parse_qs

app = FastAPI()

templates = Jinja2Templates(directory="templates")
select_iri = "http://10.218.121.139:7200/repositories/MatCHMaker"
update_iri = "http://10.218.121.139:7200/repositories/MatCHMaker/statements"


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Main Page with file upload"""
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/uploadDocumentation/")
async def upload_Documentation(
    request: Request, file: UploadFile = File(None), url: str = Form(None)
):
    """Add Documentation from an Excel sheet"""
    ts = Triplestore("sparqlwrapper", base_iri=select_iri, update_iri=update_iri)
    if file and file.filename.endswith((".xls", ".xlsx", ".csv")):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        try:
            td = TableDoc.parse_csv(temp_file_path)
            td.save(ts)
        finally:
            os.remove(temp_file_path)
            result_message = f"{file.filename if file else url} has populated the Graph"
    elif url:
        try:
            parsed_url = urlparse(url)
            file_name = os.path.basename(parsed_url.path)
            if not file_name.lower().endswith((".xls", ".xlsx", ".csv")):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file type. Please provide a valid Excel or CSV file URL.",
                )
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid URL or unable to download file.",
                        )
            td = TableDoc.parse_csv(url)
            td.save(ts)
            result_message = "The Graph is populated from the URL"
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="No file or URL provided.")

    return templates.TemplateResponse(
        "result.html", {"result_message": result_message, "request": request}
    )

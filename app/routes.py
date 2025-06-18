from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse
from app import services, models
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@router.post("/upload", response_model=models.FileProcessResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_data = await file.read()
    saved_path = services.save_upload(file_data, file.filename)
    pipelined_path = services.run_pipeline(saved_path)

    download_url=f"/download/{pipelined_path.name}"

    return templates.TemplateResponse(
        "upload_success.html",
        {
            "request": request,
            "filename": pipelined_path.name,
            "download_url": download_url
        }
    )

@router.get("/download/{filename}")
def download_file(filename: str) -> FileResponse:
    file_path = services.PROCESSED_DIR / filename

    return FileResponse(
        path=file_path, filename=filename, media_type="application/octet-stream"
    )


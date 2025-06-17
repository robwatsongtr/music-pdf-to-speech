from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app import services, models

router = APIRouter()

@router.post("/upload", response_model=models.FileProcessResponse)
async def upload_file(file: UploadFile = File(...)) -> models.FileProcessResponse:
    file_data = await file.read()
    saved_path = services.save_upload(file_data, file.filename)
    pipelined_path = services.run_pipeline(saved_path)

    return models.FileProcessResponse(
        filename=pipelined_path.name,
        download_url=f"/download/{pipelined_path.name}"
    )

@router.get("/download/{filename}")
def download_file(filename: str) -> FileResponse:
    file_path = services.PROCESSED_DIR / filename
    
    return FileResponse(
        path=file_path, filename=filename, media_type="application/octet-stream"
    )
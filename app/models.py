from pydantic import BaseModel

# Provides validation and documentation 
class FileProcessResponse(BaseModel):
    filename: str
    download_url: str

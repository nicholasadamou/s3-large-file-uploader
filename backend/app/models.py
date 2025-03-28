from pydantic import BaseModel

class StartUploadRequest(BaseModel):
    filename: str
    content_type: str
    user_id: str

class UploadPartRequest(BaseModel):
    upload_id: str
    key: str
    part_number: int
    etag: str
    user_id: str

class CompleteUploadRequest(BaseModel):
    upload_id: str
    key: str
    user_id: str
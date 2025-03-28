from fastapi import APIRouter, HTTPException
from .models import StartUploadRequest, UploadPartRequest, CompleteUploadRequest
from .database import uploads_collection
from .s3 import s3_client, S3_BUCKET_NAME

router = APIRouter()


@router.post(
    "/api/start-upload",
    summary="Initialize a multipart upload",
    description="Creates a new multipart upload session in S3 and records it in the database",
)
async def start_upload(request: StartUploadRequest):
    """
    Start a new multipart upload process:

    - Creates a multipart upload in S3
    - Records the upload session in the database
    - Returns the upload ID and key for later operations

    The client should use this endpoint before uploading any file parts.
    """
    response = s3_client.create_multipart_upload(
        Bucket=S3_BUCKET_NAME, Key=request.filename, ContentType=request.content_type
    )
    await uploads_collection.insert_one(
        {
            "user_id": request.user_id,
            "key": response["Key"],
            "upload_id": response["UploadId"],
            "parts": [],
            "status": "initiated",
        }
    )
    return {"upload_id": response["UploadId"], "key": response["Key"]}


@router.get(
    "/api/get-signed-url",
    summary="Get a pre-signed URL for part upload",
    description="Generates a pre-signed URL that allows direct upload to S3",
)
async def get_signed_url(upload_id: str, key: str, part_number: int):
    """
    Generate a pre-signed URL for uploading a specific part:

    - Creates a temporary URL valid for 1 hour
    - Client can use this URL to upload the part directly to S3
    - Part number must be between 1 and 10,000

    The client should request a new URL for each part they need to upload.
    """
    signed_url = s3_client.generate_presigned_url(
        "upload_part",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": key,
            "PartNumber": part_number,
            "UploadId": upload_id,
        },
        ExpiresIn=3600,
    )
    return {"signed_url": signed_url}


@router.post(
    "/api/upload-part",
    summary="Record a successfully uploaded part",
    description="Updates the database with information about an uploaded part",
)
async def upload_part(request: UploadPartRequest):
    """
    Record a part that was successfully uploaded to S3:

    - Updates the database with the ETag returned from S3
    - Tracks the part number for later assembly
    - Sets the upload status to "in-progress"

    The client should call this after successfully uploading a part using the pre-signed URL.
    """
    await uploads_collection.update_one(
        {
            "upload_id": request.upload_id,
            "key": request.key,
            "user_id": request.user_id,
        },
        {
            "$push": {
                "parts": {"etag": request.etag, "part_number": request.part_number}
            },
            "$set": {"status": "in-progress"},
        },
    )
    return {"success": True}


@router.post(
    "/api/complete-upload",
    summary="Complete the multipart upload",
    description="Finalizes the multipart upload by combining all parts in S3",
)
async def complete_upload(request: CompleteUploadRequest):
    """
    Complete a multipart upload by combining all uploaded parts:

    - Retrieves all parts from the database
    - Sends a complete request to S3 with all part ETags
    - Updates the upload status to "completed"
    - Returns the final S3 location of the assembled file

    This should be called after all parts have been successfully uploaded.
    """
    upload = await uploads_collection.find_one(
        {"upload_id": request.upload_id, "key": request.key, "user_id": request.user_id}
    )
    if not upload or not upload.get("parts"):
        raise HTTPException(
            status_code=404, detail="Upload session not found or no parts uploaded"
        )

    sorted_parts = sorted(upload["parts"], key=lambda x: x["part_number"])
    payload = {
        "Bucket": S3_BUCKET_NAME,
        "Key": request.key,
        "UploadId": request.upload_id,
        "MultipartUpload": {
            "Parts": [
                {"ETag": part["etag"], "PartNumber": part["part_number"]}
                for part in sorted_parts
            ]
        },
    }
    response = s3_client.complete_multipart_upload(**payload)
    await uploads_collection.update_one(
        {"upload_id": request.upload_id}, {"$set": {"status": "completed"}}
    )
    return {
        "message": "Upload completed successfully",
        "location": response["Location"],
        "key": response["Key"],
    }

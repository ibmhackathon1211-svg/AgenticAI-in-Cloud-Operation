from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from services.aws_service import get_aws_service

app = FastAPI(
    title="AWS Automation API",
    description="Real AWS tools for IBM Orchestrate / Multi-Agent System",
    version="1.0.0"
)


# ---------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------
class ResizeRequest(BaseModel):
    volume_id: str
    new_size: int


class DescribeRequest(BaseModel):
    volume_id: str


class SnapshotRequest(BaseModel):
    volume_id: str


# ---------------------------------------------------------
# REAL: RESIZE EBS VOLUME
# ---------------------------------------------------------
@app.post("/resize-ebs")
def resize_ebs(req: ResizeRequest):
    aws = get_aws_service()

    if not aws.credentials_configured:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AWS credentials not configured."
        )

    result = aws.modify_volume(req.volume_id, req.new_size)

    # Your service returns {"error": "..."} on failure
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


# ---------------------------------------------------------
# REAL: DESCRIBE EBS VOLUME
# ---------------------------------------------------------
@app.post("/describe-volume")
def describe_volume(req: DescribeRequest):
    aws = get_aws_service()

    if not aws.credentials_configured:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AWS credentials not configured."
        )

    result = aws.describe_volume(req.volume_id)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])

    return result


# ---------------------------------------------------------
# REAL: CREATE SNAPSHOT
# ---------------------------------------------------------
@app.post("/create-snapshot")
def create_snapshot(req: SnapshotRequest):
    aws = get_aws_service()

    if not aws.credentials_configured:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AWS credentials not configured."
        )

    # Now correctly calling your AWSService.create_snapshot()
    result = aws.create_snapshot(req.volume_id)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


# ---------------------------------------------------------
# HEALTH CHECK (Optional but Recommended)
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    aws = get_aws_service()
    return {
        "status": "ok",
        "aws_credentials": aws.credentials_configured,
        "region": aws.aws_region
    }

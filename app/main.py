
from fastapi import FastAPI

from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService


app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description=(
        "Publish a message across multiple platforms "
        "using one REST API endpoint."
    ),
    version="1.0.0"
)


posting_service = PostingService()


@app.get("/")
async def home():

    return {
        "message": "Automated Posting API is running",
        "docs": "/docs"
    }


@app.post(
    "/posting",
    response_model=PostingResponse
)
async def create_post(request: PostingRequest):

    result = await posting_service.publish(
        request.message
    )

    return result

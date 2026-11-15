
import re
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator


class PostingRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value):

        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty")

        if len(value) > 200:
            raise ValueError(
                "Message must not exceed 200 characters"
            )

        # Extract HTTP/HTTPS URLs
        urls = re.findall(
            r"https?://[^\s]+",
            value
        )

        if len(urls) != 1:
            raise ValueError(
                "Message must contain exactly one CTA link"
            )

        # Remove common punctuation at the end
        url = urls[0].rstrip(".,!?;:)")

        parsed = urlparse(url)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.netloc
            or "." not in parsed.netloc
        ):
            raise ValueError("Invalid URL")

        return value


class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: str | None = None
    public_access: bool = False
    date: str | None = None
    time: str | None = None
    error: str | None = None


class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]

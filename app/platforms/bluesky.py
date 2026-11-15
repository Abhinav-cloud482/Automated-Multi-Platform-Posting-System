
import httpx
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import BasePlatform


class BlueskyPlatform(BasePlatform):

    name = "Bluesky"

    async def post(self, message: str):

        if not settings.BLUESKY_HANDLE or not settings.BLUESKY_APP_PASSWORD:
            raise Exception("Bluesky credentials missing")

        async with httpx.AsyncClient(timeout=20) as client:

            # Authenticate
            auth_response = await client.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={
                    "identifier": settings.BLUESKY_HANDLE,
                    "password": settings.BLUESKY_APP_PASSWORD
                }
            )

            auth_response.raise_for_status()

            auth = auth_response.json()

            token = auth["accessJwt"]
            did = auth["did"]

            # Create post
            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            response = await client.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                json={
                    "repo": did,
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": message,
                        "createdAt": now
                    }
                }
            )

            response.raise_for_status()

            data = response.json()

            rkey = data["uri"].split("/")[-1]

            posted_url = (
                f"https://bsky.app/profile/"
                f"{settings.BLUESKY_HANDLE}/post/{rkey}"
            )

            return {
                "posted_url": posted_url,
                "public_access": True
            }

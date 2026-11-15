
import httpx

from app.config import settings
from app.platforms.base import BasePlatform


class RedditPlatform(BasePlatform):

    name = "Reddit"

    async def post(self, message: str):

        required = [
            settings.REDDIT_CLIENT_ID,
            settings.REDDIT_CLIENT_SECRET,
            settings.REDDIT_REFRESH_TOKEN,
            settings.REDDIT_SUBREDDIT
        ]

        if not all(required):
            raise Exception("Reddit credentials missing")

        async with httpx.AsyncClient(timeout=30) as client:

            # Obtain OAuth access token
            token_response = await client.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=(
                    settings.REDDIT_CLIENT_ID,
                    settings.REDDIT_CLIENT_SECRET
                ),
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": settings.REDDIT_REFRESH_TOKEN
                },
                headers={
                    "User-Agent": "AutomatedPostingApp/1.0"
                }
            )

            token_response.raise_for_status()

            access_token = token_response.json()["access_token"]

            # Submit text post
            response = await client.post(
                "https://oauth.reddit.com/api/submit",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": "AutomatedPostingApp/1.0"
                },
                data={
                    "api_type": "json",
                    "kind": "self",
                    "sr": settings.REDDIT_SUBREDDIT,
                    "title": "New Update",
                    "text": message
                }
            )

            response.raise_for_status()

            data = response.json()

            errors = data.get("json", {}).get("errors", [])

            if errors:
                raise Exception(str(errors))

            post_data = data.get("json", {}).get("data", {})

            return {
                "posted_url": post_data.get("url"),
                "public_access": bool(post_data.get("url"))
            }

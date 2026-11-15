
import httpx

from app.config import settings
from app.platforms.base import BasePlatform


class MastodonPlatform(BasePlatform):

    name = "Mastodon"

    async def post(self, message: str):

        if not settings.MASTODON_INSTANCE or not settings.MASTODON_ACCESS_TOKEN:
            raise Exception("Mastodon credentials missing")

        instance = settings.MASTODON_INSTANCE.rstrip("/")

        async with httpx.AsyncClient(timeout=20) as client:

            response = await client.post(
                f"{instance}/api/v1/statuses",
                headers={
                    "Authorization": (
                        f"Bearer {settings.MASTODON_ACCESS_TOKEN}"
                    )
                },
                json={
                    "status": message,
                    "visibility": "public"
                }
            )

            response.raise_for_status()

            data = response.json()

            return {
                "posted_url": data.get("url"),
                "public_access": (
                    data.get("visibility") == "public"
                    and bool(data.get("url"))
                )
            }

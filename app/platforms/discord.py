
import httpx

from app.config import settings
from app.platforms.base import BasePlatform


class DiscordPlatform(BasePlatform):

    name = "Discord"

    async def post(self, message: str):

        if not settings.DISCORD_WEBHOOK_URL:
            raise Exception("Discord webhook missing")

        async with httpx.AsyncClient(timeout=20) as client:

            response = await client.post(
                settings.DISCORD_WEBHOOK_URL,
                params={"wait": "true"},
                json={
                    "content": message
                }
            )

            response.raise_for_status()

            data = response.json()

            message_id = data["id"]
            channel_id = (
                data.get("channel_id")
                or settings.DISCORD_CHANNEL_ID
            )

            posted_url = None

            if channel_id:
                posted_url = (
                    f"https://discord.com/channels/"
                    f"@me/{channel_id}/{message_id}"
                )

            return {
                "posted_url": posted_url,
                "public_access": False
            }

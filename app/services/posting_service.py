
from datetime import datetime, timezone

from app.platforms.bluesky import BlueskyPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.discord import DiscordPlatform


class PostingService:

    def __init__(self):

        self.platforms = [
            BlueskyPlatform(),
            MastodonPlatform(),
            RedditPlatform(),
            TelegramPlatform(),
            DiscordPlatform()
        ]

    async def publish(self, message: str):

        results = []

        for platform in self.platforms:

            try:

                result = await platform.post(message)

                current_time = datetime.now(timezone.utc)

                results.append({
                    "platform": platform.name,
                    "status": "success",
                    "posted_url": result.get("posted_url"),
                    "public_access": result.get(
                        "public_access", False
                    ),
                    "date": current_time.strftime("%Y-%m-%d"),
                    "time": current_time.strftime("%H:%M:%S"),
                    "error": None
                })

            except Exception as error:

                results.append({
                    "platform": platform.name,
                    "status": "failed",
                    "posted_url": None,
                    "public_access": False,
                    "date": None,
                    "time": None,
                    "error": str(error)
                })

        return {
            "success": any(
                item["status"] == "success"
                for item in results
            ),
            "results": results
        }

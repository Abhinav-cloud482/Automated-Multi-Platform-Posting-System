
import httpx

from app.config import settings
from app.platforms.base import BasePlatform


class TelegramPlatform(BasePlatform):

    name = "Telegram"

    async def post(self, message: str):

        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            raise Exception("Telegram credentials missing")

        api_url = (
            f"https://api.telegram.org/bot"
            f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        async with httpx.AsyncClient(timeout=20) as client:

            response = await client.post(
                api_url,
                json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message
                }
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("ok"):
                raise Exception(data.get("description", "Telegram failed"))

            result = data["result"]

            message_id = result["message_id"]

            username = settings.TELEGRAM_CHANNEL_USERNAME

            posted_url = None

            if username:
                posted_url = (
                    f"https://t.me/{username.lstrip('@')}/{message_id}"
                )

            return {
                "posted_url": posted_url,
                "public_access": bool(posted_url)
            }

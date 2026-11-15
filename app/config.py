
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Bluesky
    BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
    BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

    # Mastodon
    MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE")
    MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")

    # Reddit
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_REFRESH_TOKEN = os.getenv("REDDIT_REFRESH_TOKEN")
    REDDIT_SUBREDDIT = os.getenv("REDDIT_SUBREDDIT")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_CHANNEL_USERNAME = os.getenv(
        "TELEGRAM_CHANNEL_USERNAME"
    )

    # Discord
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")


settings = Settings()

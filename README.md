
# Automated Multi-Platform Posting System

A Python application built using FastAPI that allows
users to publish a single message across multiple
third-party platforms through one REST API endpoint.

## Technologies

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- REST APIs

## Supported Platforms

1. Bluesky
2. Mastodon
3. Reddit
4. Telegram
5. Discord

## Features

- Single API endpoint for multi-platform posting.
- Message validation.
- Maximum 200-character limit.
- Exactly one CTA URL required.
- Independent platform integrations.
- Individual error handling.
- Publishing status for each platform.
- Environment-based API credentials.

## Project Setup

Clone the repository:

    git clone YOUR_REPOSITORY_URL

Navigate into the project:

    cd automated-posting

Create virtual environment:

    python -m venv venv

Activate virtual environment:

Windows:

    venv\Scripts\activate

Linux/Mac:

    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Configure credentials:

Copy .env.example to .env and enter your API credentials.

## Run Application

    uvicorn app.main:app --host 0.0.0.0 --port 4000

## API Documentation

Open:

    http://localhost:4000/docs

## API Endpoint

POST /posting

Example Request:

    {
      "message": "Check out our latest platform https://example.com"
    }

## Testing

Run:

    pytest -v

## Security

API credentials are stored in environment variables.
Never commit the .env file or private credentials.

## Author

Abhinav Dixit
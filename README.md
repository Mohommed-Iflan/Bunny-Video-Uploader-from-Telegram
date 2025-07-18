# Bunny Storage Video Upload Bot

A Telegram bot that receives videos (300-500MB) and uploads them to Bunny Storage.

## Features
- Receives videos via Telegram
- Validates file size (300-500MB)
- Uploads to Bunny Storage
- Hosted on Railway

## Setup

1. Clone this repository
2. Create `.env` file based on `.env.example`
3. For Python:
   ```bash
   pip install -r requirements.txt
   python src/app.py
from flask import Flask, request, jsonify
from bot import VideoUploadBot
import os

app = Flask(__name__)
bot = VideoUploadBot(os.getenv('TELEGRAM_TOKEN'))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot.updater.bot)
    bot.dispatcher.process_update(update)
    return jsonify(success=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    webhook_url = f"https://{os.getenv('RAILWAY_PROJECT_NAME')}.up.railway.app/webhook"
    bot.start_webhook(webhook_url, port)
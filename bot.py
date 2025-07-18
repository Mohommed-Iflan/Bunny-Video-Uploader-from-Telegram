from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from utils.storage import upload_to_bunny
import os
import tempfile

class VideoUploadBot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        # Add handlers
        self.dispatcher.add_handler(
            MessageHandler(Filters.video, self.handle_video)
        )
    
    def start_webhook(self, webhook_url, port):
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=self.token,
            webhook_url=webhook_url
        )
        self.updater.idle()
    
    def handle_video(self, update: Update, context: CallbackContext):
        bot = context.bot
        message = update.message
        
        if message.video:
            video = message.video
            file_id = video.file_id
            file_size = video.file_size
            
            # Validate file size (300-500MB)
            if file_size < 300*1024*1024 or file_size > 500*1024*1024:
                bot.send_message(
                    chat_id=message.chat_id,
                    text="Please send a video between 300MB and 500MB"
                )
                return
            
            try:
                # Create temp file
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Download from Telegram
                file = bot.get_file(file_id)
                file.download(custom_path=temp_path)
                
                # Upload to Bunny
                filename = f"video_{file_id}.mp4"
                if upload_to_bunny(temp_path, filename):
                    bot.send_message(
                        chat_id=message.chat_id,
                        text="Video uploaded successfully to Bunny Storage!"
                    )
                else:
                    bot.send_message(
                        chat_id=message.chat_id,
                        text="Failed to upload video to Bunny Storage"
                    )
                
            except Exception as e:
                bot.send_message(
                    chat_id=message.chat_id,
                    text=f"Error processing video: {str(e)}"
                )
            
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

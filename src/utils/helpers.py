import os

def validate_file_size(file_size):
    """Check if file is between 300-500MB"""
    return 300*1024*1024 <= file_size <= 500*1024*1024

def generate_filename(file_id):
    """Generate unique filename for storage"""
    return f"video_{file_id}.mp4"

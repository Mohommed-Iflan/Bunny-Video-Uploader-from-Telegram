import requests
import os
from typing import Tuple

def upload_to_bunny(file_path: str, filename: str) -> Tuple[bool, str]:
    """Upload file to Bunny Storage"""
    api_key = os.getenv('BUNNY_API_KEY')
    storage_zone = os.getenv('BUNNY_STORAGE_ZONE')
    region = os.getenv('BUNNY_REGION', 'ny')
    
    url = f"https://{region}.storage.bunnycdn.com/{storage_zone}/{filename}"
    headers = {
        "AccessKey": api_key,
        "Content-Type": "application/octet-stream"
    }
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.put(url, headers=headers, data=f)
        
        if response.status_code == 201:
            return True, f"https://{storage_zone}.b-cdn.net/{filename}"
        return False, f"Upload failed with status {response.status_code}"
    except Exception as e:
        return False, str(e)
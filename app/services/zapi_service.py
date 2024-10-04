import requests
import os
from dotenv import load_dotenv
from app.utils.database import get_user

zapi_token = os.getenv("ZAPI_TOKEN")
zapi_id = os.getenv("ZAPI_ID")

async def send_message(phone: str, message: str):
    url = f"https://api.z-api.io/instances/{zapi_id}/token/{zapi_token}/send-text"
    response = requests.post(url, json={"phone": phone, "message": message})
    return response.status_code


async def get_user_thread_id(phone: str):
    user = await get_user(phone)
    return user.thread_id
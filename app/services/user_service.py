from app.utils.database import get_user, insert_user
from app.services.openai_service import create_thread
import json


async def get_user_thread_id(phone: str):
    user = await get_user(phone)
    if user is not None:
        return user["thread_id"]
    else:
        return None


async def check_user_is_new(phone: str):
    user = await get_user_thread_id(phone)
    if user is None:
        return True
    return False


async def create_user(phone: str, assistant_id: str):
    thread = await create_thread()
    await insert_user(phone, assistant_id, thread.id)
    return True
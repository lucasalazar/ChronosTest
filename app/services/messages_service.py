from app.services.user_service import get_user_thread_id, check_user_is_new, create_user
from app.services.openai_service import create_thread, create_message, run_message
import os
from datetime import datetime

assistant_id = os.getenv("WEATHER_ASSISTANT_ID")
data = datetime.now()

async def process_message(phone : str, message: str):
    if await check_user_is_new(phone):
        if await create_user(phone, assistant_id):
            thread_id = await get_user_thread_id(phone)
            message = await create_message(thread_id, "user", message + f" a data de hoje é {data}")
            run = await run_message(thread_id, assistant_id, phone)
            print(run.data[0].content[0].text.value)
    else:
        thread_id = await get_user_thread_id(phone)
        message = await create_message(thread_id, "user", message + f" a data de hoje é {data}")
        run = await run_message(thread_id, assistant_id, phone)
        print(run.data[0].content[0].text.value)
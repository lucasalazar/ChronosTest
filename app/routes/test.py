from fastapi import APIRouter
from app.services.openai_service import create_assistant, create_thread, create_message, run_message

router = APIRouter()

@router.get("/")
async def test():
    thread = await create_thread()
    message = await create_message("thread_t2kTjuuyniL0KNQo40QZ7ae7", "user", "Aqui pra belo horizonte")
    run = await run_message("thread_t2kTjuuyniL0KNQo40QZ7ae7", "asst_Bz9cEgXxey0R5FhV7rYiiBqt")
    
    return {"thread": thread, "message": message,"run": run}
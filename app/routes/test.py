from fastapi import APIRouter
from app.services.openai_service import assistant_chat

router = APIRouter()

@router.get("/")
async def test():
    return await assistant_chat("5585981811515", "Olá, tudo bem? você gosta de biscoito?")
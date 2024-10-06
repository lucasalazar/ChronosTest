from fastapi import APIRouter, Request
from app.services.messages_service import process_message
import json
import os


router = APIRouter()

@router.post("/receivemessage/")
async def receive_message(request: Request):
    payload = await request.json()
    print(payload["phone"])
    if payload["phone"] is not None and (payload["phone"] == "558581811515" or payload["phone"] == "554137950674"):
        await process_message(payload["phone"], payload["text"]["message"])
    
    # print("Webhook data received: ", json.dumps(payload, indent=4))
    


from fastapi import HTTPException
from openai import OpenAI
import json
from datetime import datetime
from app.services.weather_service import get_weather_data
from app.services.zapi_service import send_message


client = OpenAI()

data = datetime.now()


async def get_weather(location: str, date_formatted: str):
    return await get_weather_data(location, date_formatted)

async def create_assistant():
    try:
        assistant = client.beta.assistants.create(
            model="gpt-3.5-turbo",
            name="Weather Assistant",
            instructions="Você é um assistente que pode chamar funções externas para buscar informações sobre previsão do tempo. Pergunte o nome do usuário e armazene isso para usar depois no fluxo, priorize por chamar ele pelo nome quando achar necessário.",
            tools=[
                {
                "type": "function",
                "function": {
                    "name": "get_weather_data",
                    "description": "Função para pegar os dados de previsão do tempo",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                        "type": "string",
                        "description": "Localização para buscar a previsão do tempo"
                        },
                        "date_formatted": {
                        "type": "string",
                        "description": "A data solicitada pelo usuário formatada no modelo yyyy-M-d['T'H:m:s][.SSS][X] para buscar a previsão do tempo"
                        }
                    },
                    "required": ["location", "date_formatted"],
                    "additionalProperties": False
                    },
                    "strict": True
                }
                },
            ]
        )
            
           
        return assistant

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def create_thread():
    try:
        thread = client.beta.threads.create()

        return thread

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
async def create_message(thread_id: str, role: str, content: str):
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )

        return message

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def run_message(thread_id: str, assistant_id: str, phone: str):
    try:
        print("Running message", phone)
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        if run.status == 'completed':
            print("Run completed", phone)
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            await send_message(phone, messages.data[0].content[0].text.value)
            return messages
        
        tool_outputs = []
        
        if run.required_action is not None:
            print("Run required action", phone)
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                print("Function name",tool.function.name)
                if tool.function.name == "get_weather_data":
                    data = await get_weather(json.loads(tool.function.arguments)["location"], json.loads(tool.function.arguments)["date_formatted"])
                    tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": data
                    })
                    
            
        if tool_outputs:
            try:
                print("Submitting tool outputs", phone)
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
                )
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        
        if tool_outputs:
            if run.status == 'completed':
                print("Run completed", phone)
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                await send_message(phone, messages.data[0].content[0].text.value)
                print(messages.data[0].content[0].text.value)
                return messages

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
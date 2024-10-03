from fastapi import HTTPException
import openai
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

user_data = {}

async def get_external_data(location: str, date_formatted: str):
    print(date_formatted)
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date_formatted}?unitGroup=metric&key={weather_api_key}&contentType=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar API externa")
    
    tempeature_info = response.json()["days"][0]
    location = response.json()["resolvedAddress"]
    
    return f"informações de temperatura: {tempeature_info}, temp é a temperatura média. localização solicitada: {location}"

async def assistant_chat(user_number: str, user_input: str):
    try:
        current_dateTime = datetime.now()
        messages = [
            {"role": "system", "content": f"Você é um assistente que pode chamar funções externas para buscar as informações sobre previsão do tempo. a data atual é ${current_dateTime}."},
            {"role": "user", "content": user_input}
        ]

        functions = [
            {
                "name": "get_external_data",
                "description": "Busca dados da API externa baseada no parâmetro fornecido",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "A localização de onde o usuário quer buscar a previsão do tempo"
                        },
                        "date_formatted": {
                            "type": "string",
                            "description": "A data solicitada pelo usuário formatada no modelo yyyy-M-d['T'H:m:s][.SSS][X] para buscar a previsão do tempo"
                        }
                    },
                    "required": ["location", "date_formatted"]
                }
            }
        ]

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        if response.choices[0].finish_reason == 'function_call':
            function_call_info = response.choices[0].message.function_call
            function_name = function_call_info.name
            function_args = json.loads(function_call_info.arguments)

            if function_name == "get_external_data":
                data = await get_external_data(function_args["location"], function_args["date_formatted"])

                interpretation_prompt = (
                    f"A resposta da função é:\n{json.dumps(data)}\n"
                    "Por favor, extraia as informações de temperatura e as condições meteorológicas da data solicitada, traduza para português e também fale a cidade que foi solicitada. Sempre seja gentil e utilize emojis quando achar necessário."
                )

                interpretation_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": interpretation_prompt}
                    ]
                )

                extracted_value = interpretation_response.choices[0].message.content

                return {
                    "message": "Função chamada com sucesso",
                    "extracted_info": extracted_value
                }

        return {"message": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
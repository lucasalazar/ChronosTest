import requests
import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")

async def get_weather_data(location: str, date_formatted: str):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date_formatted}?unitGroup=metric&key={weather_api_key}&contentType=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar API externa")
    
    temperature_info = response.json()["days"][0]
    location = response.json()["resolvedAddress"]
    
    return f"Informações de temperatura: {temperature_info}, temp é a temperatura média. Localização solicitada: {location}"
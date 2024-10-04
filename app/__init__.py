from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import messages_route
from app.utils.database import create_db

app = FastAPI()
create_db()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages_route.router)
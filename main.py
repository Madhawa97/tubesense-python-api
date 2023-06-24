from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import poe
import os

token = os.getenv('POE_TOKEN')
client = poe.Client(token)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Body(BaseModel):
    prompt: str

@app.post('/')
def root(body:Body):

    prompt = body.prompt
    for chunk in client.send_message("a2", prompt):
        pass
    print(chunk["text"])

    return chunk["text"]
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import poe
import os
import re

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
    comments: str


@app.post('/')
def root(body: Body):

    comments = body.comments

    if not comments:
        return {"error": "comments not present."}

    received_response = get_preception(comments)
    
    if not received_response:
        return {"error": "connection with poe failed."}
    
    extracted_preception = extract_preception(received_response)

    if not extracted_preception:
        return {"error": "preception extraction failed."}

    return {"result": extracted_preception}


def get_preception(comments):
    prompt = '''# Preception \n Please analyze the following comments from a YouTube video and rate the perception of the video on a scale of 1 to 5, where 1 is very bad, 2 is bad, 3 is neutral, 4 is good, and 5 is very good. The perception should reflect the overall sentiment, tone, and attitude of the comments towards the video. Please output your answer in the format of { "perception":"X" }, where X is the perception score. \n # Comments \n''' + \
        comments + \
        '''\n # Important \n Please output your answer in the format of { "perception":"X" }, where X is the perception score.'''
    for chunk in client.send_message("a2", prompt):
        pass
    return chunk["text"]


def extract_preception(response_string):
    match = re.search(r"perception.*?(\d)", response_string)

    if match:
        perception = match.group(1)
        return perception
    else:
        return None
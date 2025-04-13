### BACKEND (FastAPI) ###

# backend/main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import base64

app = FastAPI()

# CORS per collegarsi dal frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = "TUA_CHIAVE_API"

@app.post("/chat")
async def chat(text: str = Form(...), image: UploadFile = File(...)):
    image_data = await image.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")
    image_url = f"data:{image.content_type};base64,{base64_image}"

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ],
        max_tokens=1000
    )

    reply = response.choices[0].message["content"]
    return {"response": reply}


# backend/requirements.txt
fastapi
uvicorn
python-multipart
openai


# backend/render.yaml
services:
  - type: web
    name: gpt4-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port 10000"
    plan: free
    region: frankfurt


from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import openai
import base64
import os

# CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # per lo sviluppo, puoi restringere in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API key da variabile d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    if not text and not image:
        return {"response": "Inserisci almeno testo o immagine"}

    messages = []

    if text:
        messages.append({"type": "text", "text": text})

    if image:
        content = await image.read()
        base64_img = base64.b64encode(content).decode("utf-8")
        image_url = f"data:{image.content_type};base64,{base64_img}"
        messages.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[{"role": "user", "content": messages}],
            max_tokens=1000
        )
        reply = completion.choices[0].message["content"]
        return {"response": reply}
    except Exception as e:
        print("Errore OpenAI:", e)
        return {"response": "Errore durante la richiesta a OpenAI"}

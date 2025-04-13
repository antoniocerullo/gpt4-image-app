from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated
from openai import OpenAI
import base64
import os
import traceback

# Inizializza FastAPI
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key di OpenAI da variabile d’ambiente
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Route /chat
@app.post("/chat")
async def chat(
    text: Annotated[Optional[str], Form()] = None,
    image: Annotated[Optional[UploadFile], File()] = None
):
    
    print("📥 Ricevuto:")
    print(f"text: {text}")
    print(f"image: {image.filename if image else 'nessuna immagine'}")
    
    if not text and not image:
        return {"response": "Inserisci almeno testo o immagine"}
    try:
           if image:
            content = await image.read()
            base64_img = base64.b64encode(content).decode("utf-8")
            image_url = f"data:{image.content_type};base64,{base64_img}"
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": text or ""},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }]
        else:
            messages = [{"role": "user", "content": text}]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )

        return {"response": response.choices[0].message.content}
   
    except Exception as e:
        print("❌ Errore durante la richiesta a OpenAI:")
        traceback.print_exc()
        return {"response": f"Errore durante la richiesta a OpenAI: {str(e)}"}

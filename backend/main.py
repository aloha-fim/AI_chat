# uvicorn main:app
# uvicorn main:app --reload

#import backend modules
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai


# Customer function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages


# Get Environment Vars
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


#set variable to function
app = FastAPI()


# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:2173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# api routes
@app.get("/")
async def root():
    print("fred")
    return {"message": "Hello Fred"}

# Config Routes
# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}

# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}


@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # decode audio by converting audio into text format
    message_decoded = convert_audio_to_text(audio_input)

    # guard: ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # get chat response by taking audio input into text
    chat_response = get_chat_response(message_decoded)

    # store messages of input text converted from audio and chatgpt response
    store_messages(message_decoded, chat_response)

    # guard: ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")


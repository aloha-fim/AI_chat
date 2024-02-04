import openai
from decouple import config

from functions.database import get_recent_messages


# Retrieve Environement Variables from OpenAI
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Open AI - Whisper
# Convert audio of what I speak from recording to text in IDE.
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        return

# Open AI - ChatGPT
# Takes text from audio recording and feeds to chatGPT
def get_chat_response(message_input):

    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input + "Only say less than 5 words in Korean if speaking in Korean.  The remaining words should be in English"}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=messages
        )
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        return

from openai import AsyncOpenAI
import os

from config import *


client = AsyncOpenAI(api_key=TOKIFY_API_KEY, base_url=TOKIFY_BASE_URL)

async def voice2text(destination):
    audio_file = open(destination, "rb")

    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    audio_file.close()

    return transcript.text

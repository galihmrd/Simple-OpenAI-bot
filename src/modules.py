import os
import openai
from pyrogram import Client, filters
from config import OPEN_AI_API


async def openAI(prompt)
    openai.api_key = OPEN_AI_API
    response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=300)
    await message.reply(response["choices"][0]["text"])

@Client.on_message(filters.command("tanya"))
async def tanyabot(client, message):
    prompt = " ".join(message.command[1:])
    await openAI(prompt)

import os
import openai
from pyrogram import Client, filters
from config import OPEN_AI_API


async def openAI(self, msg):
    openai.api_key = OPEN_AI_API
    try:
       response = openai.Completion.create(model="text-davinci-003", prompt=self, temperature=0.13, max_tokens=700)
    except:
       pass
    await msg.edit(response["choices"][0]["text"])

@Client.on_message(filters.command("tanya") & filters.group)
async def tanyabot(client, message):
    prompt = " ".join(message.command[1:])
    msg = await message.reply("Processing...")
    await openAI(prompt, msg)


@Client.on_message(filters.text & filters.private)
async def tanyabot_priv(client, message):
    prompt = message.text
    msg = await message.reply("Processing...")
    await openAI(prompt, msg)

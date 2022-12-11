import os
import openai
from pyrogram import Client, filters
from config import OPEN_AI_API, USERNAME_BOT


async def openAI(self, msg):
    openai.api_key = OPEN_AI_API
    try:
       response = openai.Completion.create(model="text-davinci-003", prompt=self, temperature=0.13, max_tokens=700)
    except:
       pass
    await msg.edit(response["choices"][0]["text"])

@Client.on_message(filters.text & filters.group)
async def tanyabot(client, message):
    prompt = message.text
    replied = message.reply_to_message
    if prompt.startswith(f"@{USERNAME_BOT}"):
       msg = await message.reply("Processing...")
       await openAI(prompt, msg)
    elif replied.text:
       input = prompt + " " + replied.text
       msg = await message.reply("Processing...")
       await openAI(input, msg)

@Client.on_message(filters.text & filters.private)
async def tanyabot_priv(client, message):
    prompt = message.text
    msg = await message.reply("Processing...")
    await openAI(prompt, msg)

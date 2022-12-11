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
    if not replied:
       if prompt.startswith(f"@{USERNAME_BOT}"):
          input = prompt.split(' ', 1)[1]
          msg = await message.reply("Processing...")
          await openAI(input, msg)
    elif replied.text:
       input = prompt + " " + replied.text
       if input.startswith(f"@{USERNAME_BOT}"):
          final_input = input.split(' ', 1)[1]
          msg = await message.reply("Processing...")
          await openAI(final_input, msg)

@Client.on_message(filters.text & filters.private)
async def tanyabot_priv(client, message):
    replied = message.reply_to_message
    prompt = message.text
    if not replied:
       if prompt.startswith("/start"):
          msgs = "Berikan pesan sambutan singkat"
          msg = await message.reply("Hallo!")
          await openAI(msgs, msg)
       else:
          msg = await message.reply("Processing...")
          await openAI(prompt, msg)
    elif replied.text:
       input = prompt + " " + replied.text
       msg = await message.reply("Processing...")
       await openAI(input, msg)

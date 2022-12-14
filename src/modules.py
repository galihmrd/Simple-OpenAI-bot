import os
import openai
import requests
import pytesseract
from PIL import Image
from requests import post
from pyrogram import Client, filters
from config import OPEN_AI_API, USERNAME_BOT


async def openAI(self, msg, code=None):
    openai.api_key = OPEN_AI_API
    response = openai.Completion.create(model="text-davinci-003", prompt=self, temperature=0.13, max_tokens=700)
    if code:
       code_url = (
               post(
                   "https://nekobin.com/api/documents",
                   json={"content": response["choices"][0]["text"]},
               )
               .json()
               .get("result")
               .get("key")
       )
       await msg.edit(f"**Code:** https://nekobin.com/{code_url}")
    else:
       await msg.edit(response["choices"][0]["text"], disable_web_page_preview=True)

@Client.on_message(filters.text & filters.group)
async def tanyabot(client, message):
    prompt = message.text
    replied = message.reply_to_message
    if not replied:
       if prompt.startswith(f"@{USERNAME_BOT}"):
          input = prompt.split(' ', 1)[1]
          msg = await message.reply("Processing...")
          await openAI(input, msg)
       elif prompt.startswith("@write"):
          input = "write " + prompt.split(' ', 1)[1]
          msg = await message.reply("Writing Code...")
          await openAI(input, msg, True)
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

@Client.on_message(filters.photo & filters.private)
async def ocrAI(client, message):
    photo = message.photo
    lang_code = "eng"
    tessdataUrl = f"https://github.com/galihmrd/tessdata/raw/main/{lang_code}.traineddata"
    dirs = r"./data/tessdata"
    path = os.path.join(dirs, f"{lang_code}.traineddata")
    if not os.path.exists(path):
        data = requests.get(
            tessdataUrl, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
        )
        if data.status_code == 200:
            open(path, "wb").write(data.content)
        else:
            return await message.reply(
                "`Kode bahasa salah, atau tidak didukung!`"
            )
    try:
       msg = await message.reply("Image Processing...")
       rawImage = await client.download_media(message.photo, file_name=f"{message.photo.file_id}.jpg")
       img = Image.open(rawImage)
       text = pytesseract.image_to_string(img, lang=f"{lang_code}")
       try:
          await msg.edit(f"**Optical Character Recognition**\n\n`{text[:-1]}`")
          os.remove(rawImage)
       except MessageEmpty:
                return await message.reply("Image Processing Failed!")
    except Exception as e:
       await message.reply(f"Error!\n{e}")

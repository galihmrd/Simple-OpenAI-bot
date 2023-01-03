import os
import openai
import requests
import pytesseract
from PIL import Image
from requests import post
from pyrogram import Client, filters
from config import OPEN_AI_API, USERNAME_BOT


async def openAI(self, msg, requested_by, code=None):
    openai.api_key = OPEN_AI_API
    response = openai.Completion.create(model="text-davinci-003", prompt=self, temperature=0.13, max_tokens=450)
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
       await msg.edit(f"**Code:** https://nekobin.com/{code_url}", disable_web_page_preview=True)
    else:
       await msg.edit(f"{response['choices'][0]['text']}\n\n**Requested by:** {requested_by}\n**Site:** simple-openai-web.pages.dev")

async def kbbi(input, msg, requested_by):
    api = f"https://kamus-kbbi.cyclic.app/entri/{input}"
    try:
       response = request.urlopen(api)
       data = json.loads(response.read())
       await msg.edit(f"**KBBI:** `{input}`\n\n{value['data'][0]['arti'][0]['deskripsi']}\n\n**Requested by:** {requested_by}\n**Site:** kbbi.kemdikbud.go.id")
    except Exception as e:
       await msg.edit(f"**Error:** {e}")

@Client.on_message(filters.text & filters.group)
async def tanyabot(client, message):
    prompt = message.text
    replied = message.reply_to_message
    requested_by = message.from_user.mention
    if not replied:
       if prompt.startswith(f"@{USERNAME_BOT}"):
          input = prompt.split(' ', 1)[1]
          msg = await message.reply(f"**Processing...**\n**Query:** {input}")
          await openAI(input, msg, requested_by)
       elif prompt.startswith("@write"):
          input = "write " + prompt.split(' ', 1)[1]
          msg = await message.reply(f"**Writing Code...**\n**Query:** {input}")
          await openAI(input, msg, requested_by, True)
       elif prompt.startswith("@kbbi"):
          input = prompt.split(' ', 1)[1]
          msg = await message.reply(f"**Peocessing API...\n**Query:** {input}")
          await kbbi(input, msg, requested_by)
    elif replied.photo:
       if prompt.startswith("@ocr"):
          try:
             lang_code = prompt.split(' ', 1)[1]
          except:
             lang_code = "eng"
          msg = await message.reply("Downloading...")
          photo = await client.download_media(replied.photo, file_name=f"{replied.photo.file_id}.jpg")
          await ocrAI(photo, msg, lang_code)
    elif replied.text:
       input = prompt + " " + replied.text
       if input.startswith(f"@{USERNAME_BOT}"):
          final_input = input.split(' ', 1)[1]
          msg = await message.reply(f"**Processing...**\n**Query:** {final_input}")
          await openAI(final_input, msg, requested_by)

@Client.on_message(filters.text & filters.private)
async def tanyabot_priv(client, message):
    replied = message.reply_to_message
    prompt = message.text
    requested_by = message.from_user.mention
    if not replied:
       if prompt.startswith("/start"):
          msgs = "Berikan pesan sambutan singkat"
          msg = await message.reply("Hallo!")
          await openAI(msgs, msg, requested_by)
       elif prompt.startswith("@write"):
          input = "write " + prompt.split(' ', 1)[1]
          msg = await message.reply(f"**Writing Code...**\n**Query:** {input}")
          await openAI(input, msg, requested_by, True)
       elif prompt.startswith("@kbbi"):
          input = prompt.split(' ', 1)[1]
          msg = await message.reply(f"**Peocessing API...\n**Query:** {input}")
          await kbbi(input, msg, requested_by)
       else:
          msg = await message.reply("**Processing...**\n**Query:** {prompt}")
          await openAI(prompt, msg, requested_by)
    elif replied.text:
       input = prompt + " " + replied.text
       msg = await message.reply(f"**Processing...**\n**Query:** {input}")
       await openAI(input, msg, requested_by)


async def ocrAI(photo, msg, lang_code):
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
       await msg.edit("Image Processing...")
       img = Image.open(photo)
       text = pytesseract.image_to_string(img, lang=f"{lang_code}")
       try:
          await msg.edit(f"`{text[:-1]}`")
          os.remove(rawImage)
       except:
          pass
    except Exception as e:
       await message.reply(f"Error!\n{e}")

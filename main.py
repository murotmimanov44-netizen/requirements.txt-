import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# Бул жерге өзүңүздүн маалыматтарыңызды жазыңыз
API_ID = 1234567  # Өзүңүздүн API ID'ңизди коюңуз
API_HASH = "сенин_api_hash_бул_жерге"
BOT_TOKEN = "сенин_бот_токен_бул_жерге"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

@app.on_message(filters.command("argen") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        return await message.reply("Ырдын атын жазыңыз. Мисалы: `/argen Гулжигит`")
    
    query = " ".join(message.command[1:])
    m = await message.reply("Издеп жатам...")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        url = info['url']
        title = info['title']

    await call_py.join_group_call(
        message.chat.id,
        AudioPiped(url)
    )
    await m.edit(f"Азыр ырдап жатат: {title}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    await call_py.leave_group_call(message.chat.id)
    await message.reply("Музыка токтотулду.")

call_py.start()
app.run()

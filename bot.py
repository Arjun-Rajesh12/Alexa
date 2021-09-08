# created by @Oxidisedman🔥
# open source bot 👻
# fell free and modify under the license
# importing library

import asyncio
import math
import json
import time
import shutil
import heroku3
import requests
import random
import os
import youtube_dl
from youtubesearchpython import SearchVideos
from youtube_search import YoutubeSearch
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle
)
#import script 🎭

from script import Script

#pyrogram 🔥    
alexa = Client(
    "Oxidised man",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


#contants

HELP_MESSAGE ="**hello** {}, **I'm Alexa. I'm a music bot written in** __python__ **using** __pyrogram__."
START_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("♻️ Creator", callback_data="creator"),InlineKeyboardButton("🌀 Souce code", url="https://github.com/Oxidisedman/Alexa")],[InlineKeyboardButton("🙄help", callback_data="help"),InlineKeyboardButton("devloper", url="https://t.me/Oxidisedman")],[InlineKeyboardButton("🎭Updates", url="https://t.me/tg_kid")]])
HELP_TEXT ="🙄എന്തിനോ വേണ്ടി ഓടുന്ന ബോട്ട്"
HELP_STICKER ="CAACAgUAAxkBAAFIXnZhLFpHWPsw0DiXDhIF2PMpwwQXWAACwQQAAtpZTQ8SQOsZYGo9wyAE"
ABOUT_STRING ="**hello** {}, **I'm Alexa**. --> devloped by **__@Oxidisedman__**"
START_TEXT ="__please wait__"

# filters

@alexa.on_message(filters.command('start') & filters.private)
async def start(bot, update):
    await bot.send_message(
    chat_id=update.chat.id,
    text=HELP_MESSAGE.format(update.from_user.mention),
    reply_markup=START_BUTTONS
)
@alexa.on_message(filters.command('help') & filters.private)
async def help(_, message):
    await message.reply_text("☹️ I'm created for downloading song only!")
    await message.reply_sticker(HELP_STICKER)

@alexa.on_message(filters.command(['about']))
async def about (bot, update):
      await bot.send_animation(
      animation="https://telegra.ph/file/0de87a260f415f1f92d16.mp4",
      chat_id=update.chat.id,
      caption=ABOUT_STRING.format(update.from_user.mention)
)

# callbacks

@alexa.on_callback_query()
async def cb_handler(client, query):

    if query.data == "help":
        await query.answer()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Close", callback_data="close_data")
                ]
            ]
        )

        await query.message.edit_text(
            Script.HELP_SCRIPT.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        return

    elif query.data == "creator":
         await query.answer()
         keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Close", callback_data="close_data")
                ]
            ]
        )

         await query.message.edit_text(
            Script.CREATOR.format(query.from_user.mention),
            reply_markup=keyboard,
            disable_web_page_preview=True
         )
         return

    elif query.data == "close_data":
         await query.message.delete()
        
# song plugin

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Commands

@alexa.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`Searching... Please Wait...`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            performer = f"[© @tg_kid]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**Found Literary Noting. Please Try Another Song or Use Correct Spelling!**')
            return
    except Exception as e:
        m.edit(
            "**Enter Song Name with Command!**"
        )
        print(str(e))
        return
    m.edit("`Uploading... Please Wait...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🏷 <b>Title:</b> <a href="{link}">{title}</a>\n⏳ <b>Duration:</b> <code>{duration}</code>\n👀 <b>Views:</b> <code>{views}</code>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**An Error Occured. Please try again later 🙄**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
# helpers
def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

#new plugin test

@alexa.on_message(filters.command(["vsong", "video"]))
async def ytmusic(client, message: Message):
    query = ''

    pablo = await client.send_message(
        message.chat.id, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return

    search = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**'🏷Title** `{thum}` \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` \n**Link :** `{mo}`"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {urlissed} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
alexa.run()

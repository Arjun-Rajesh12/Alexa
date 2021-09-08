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
ABOUT_STRING ="**hello** {}, **I'm Arina**. --> devloped by **__@Oxidisedman__**"
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

bin.run()

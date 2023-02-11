from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,subprocess,sys,os

try:
    import youtube_dl
except Exception as e:
    print(e)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube_dl"])
    import youtube_dl
if not os.path.exists("./mp3s"):
    os.makedirs("./mp3s")

def updateMsgs(client, message,redis):
    type = message.chat.type
    userID = message.from_user.id
    chatID = message.chat.id
    username = message.from_user.username
    text = message.text
    if username is None:
        username = "None"
    if text:
        r_1 = re.search('^تحميل (.*)$',text)
        if r_1 :
            video_url = text.replace("تحميل ","")
            r_2 = re.search('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$',video_url)
            msg = message.reply_text("يتم التحميل ⏺️")
            if r_2:
                try:
                    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
                    filename = f"./mp3s/{userID}.mp3"
                    with youtube_dl.YoutubeDL({'format':'bestaudio/best','keepvideo':False,'outtmpl':filename,}) as ydl:
                        ydl.download([video_url])
                    message.reply_audio(filename,performer=video_info["uploader"],title=video_info['title'])
                    if os.path.exists(filename):
                        os.remove(filename)
                    msg.delete()
                except Exception as e:
                    msg.edit_text("عذراً لم يتم تحميل الملف ⚠️")
                    if os.path.exists(f"./mp3s/{userID}.mp3"):
                        os.remove(f"./mp3s/{userID}.mp3")
            else:
                try:
                    video_info = youtube_dl.YoutubeDL().extract_info(f"ytsearch::{video_url}video_url",download=False)
                    filename = f"./mp3s/{userID}.mp3"
                    with youtube_dl.YoutubeDL({'format':'bestaudio/best','keepvideo':False,'outtmpl':filename,}) as ydl:
                        ydl.download([video_info["entries"][0]["webpage_url"]])
                    message.reply_audio(filename,performer=video_info["entries"][0]["uploader"],title=video_info["entries"][0]['title'])
                    if os.path.exists(filename):
                        os.remove(filename)
                    msg.delete()
                except Exception as e:
                    msg.edit_text("عذراً لم يتم تحميل الملف ⚠️")
                    if os.path.exists(f"./mp3s/{userID}.mp3"):
                        os.remove(f"./mp3s/{userID}.mp3")

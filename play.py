from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from pyrogram.types import (
     InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
)
from os import listdir
from os.path import isfile, join
def updateMsgs(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
  username = message.from_user.username
  if username is None:
    username = "None"
  userFN = message.from_user.first_name
  title = message.chat.title
  rank = isrank(redis,userID,chatID)
  text = message.text
  ADDed = """◀️꒐ بواسطه ⌁ {} 
  ✅꒐ {} بالفعل مفعله في المجموعة"""
  ADD = """◀️꒐ بواسطه ⌁ {} 
  ✅꒐ تم تفعيل {} في المجموعة"""
  unADDed = """◀️꒐ بواسطه ⌁ {} 
  ❎꒐ {} بالفعل معطله في المجموعة"""
  unADD = """◀️꒐ بواسطه ⌁ {} 
  ❎꒐ تم تعطيل {} في المجموعة"""

  if (rank is not False or rank is not  0 or rank != "vip"):

    if text == "تفعيل الالعاب" :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:gpgames".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":ADD.format(BY,R),"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":ADDed.format(BY,R),"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})

    if text == "تعطيل الالعاب" :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":unADDed.format(BY,R),"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:gpgames".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":unADD.format(BY,R),"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})

  
  games = {"rps.py":"🧱📃✂️","xo.py":"❌ ⭕️","ring.py":"👊🏻💍🖐🏻"}
  if text and re.search("^الالعاب$|^العاب$",text) and not redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID):
    tx = "🕹꒐ اليك الالعاب المقدمه من (<a href=\"http://t.me/zx_xx\">TshakeTeam</a>)"
    onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
    array = []
    if not onlyfiles:
      return False
    for f in onlyfiles:
      if f in games:
        array.append([InlineKeyboardButton(games[f],callback_data=f+"play")])
    kb = InlineKeyboardMarkup(array)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})

  if text and re.search("^نقاطي$",text):
    points = (redis.hget("{}Nbot:{}:points".format(BOT_ID,chatID),userID) or 0)
    Bot("sendMessage",{"chat_id":chatID,"text":"🔢꒐ نقاطك :- ({})".format(points),"reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})


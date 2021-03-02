from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from pyrogram import (
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
  games = {"rps.py":"🧱📃✂️","xo.py":"❌ ⭕️"}
  if text and re.search("^الالعاب$|^العاب$",text):
    tx = "🕹꒐ اليك الالعاب المقدمه من (<a href=\"http://t.me/nbbot\">NewBot</a>)"
    onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
    array = []
    if not onlyfiles:
      return False
    for f in onlyfiles:
      if f in games:
        array.append([InlineKeyboardButton(games[f],callback_data=f+"play")])
    kb = InlineKeyboardMarkup(array)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})

  if text and re.search("^نقاطي$",text):
    points = (redis.hget("{}Nbot:{}:points".format(BOT_ID,chatID),userID) or 0)
    Bot("sendMessage",{"chat_id":chatID,"text":"🔢꒐ نقاطك :- ({})".format(points),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

def updateCb(client, callback_query,redis):
  pass

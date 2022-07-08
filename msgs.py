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
  userID = message.from_user.id
  chatID = message.chat.id
  userFN = message.from_user.first_name
  rank = isrank(redis,userID,chatID)
  text = message.text


  if text and  re.search("^اضف رسائل [0-9]+$",text) and message.reply_to_message  and (rank is not False or rank is not  0 ) and rank != "admin" and rank != "owner":
    user = message.reply_to_message.from_user.id
    msgsCount = int(re.search(r'\d+', text).group())
    try:
      getUser = client.get_users(user)
      userId = getUser.id
      userFn = getUser.first_name
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
      redis.hincrby("{}Nbot:{}:msgs".format(BOT_ID,chatID),userId,msgsCount)
      Bot("sendMessage",{"chat_id":chatID,"text":f"✅꒐ تم اضافه {msgsCount} الى {userFn}","reply_to_message_id":message.id,"parse_mode":"html"})
    except Exception as e:
      Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.id,"parse_mode":"html"})


  if text == "مسح رسائلي" :
    redis.hdel("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID)
    Bot("sendMessage",{"chat_id":chatID,"text":"✅꒐ تم مسح رسائلك","reply_to_message_id":message.id,"parse_mode":"html"})
    

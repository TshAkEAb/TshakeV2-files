from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from uuid import uuid4

from pyrogram.types import (
     InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
)


def updateMsgs(client, message,redis):
  pass

def kbtotx(kb):

  tx = ""
  t = ""
  i = 0
  for n in kb:
    if n == 0:
      t +=  "◻️ "
    if n == 1:
      t +=  "❌ "
    if n == 2:
      t +=  "⭕️ "
    i += 1
    if i == 3:
      tx += "\n"+t
      t = ""
      i = 0
  return tx
def getwin(tb):
  winners=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
  win = False
  xo = "no"
  for ar in winners:
    if tb[ar[0]] == 1 and tb[ar[1]] == 1 and tb[ar[2]] ==1:
      win = True
      xo = tb[ar[0]]
      break
    if tb[ar[0]] == 2 and tb[ar[1]] == 2 and tb[ar[2]] ==2:
      win = True
      xo = tb[ar[0]]
      break
  if win == False and 0 not in tb:
    win = True
    xo = "tie"
    
  return win,xo

  

def get(client,userID,userFN,p1,p2):
  if userID == int(p1):
    fn1 = userFN
  else:
    try:
      getUser = client.get_users(int(p1))
      fn1 = getUser.first_name
    except Exception as e:
      fn1 = p1
  if userID == int(p2):
    fn2 = userFN
  else:
    try:
      getUser = client.get_users(int(p2))
      fn2 = getUser.first_name
    except Exception as e:
      fn2 = p2
  return fn1,fn2
def updateCb(client, callback_query,redis):
  if callback_query.inline_message_id:
    return False
  date = callback_query.data
  userID = callback_query.from_user.id
  userFN = callback_query.from_user.first_name
  username = callback_query.from_user.username
  chatID = callback_query.message.chat.id
  message_id = callback_query.message.id
  go = """{}꒐ ({}),❌
{}꒐ ({}),⭕️"""

  go3 = """{}꒐ ({})
{}꒐ ({})

🎊꒐ الفائز ({})"""
  go2 = """{}꒐ ({})
{}꒐ ({})

🔴꒐ تعادل"""
  if re.search("rex=",date):
    tx = callback_query.message.text
    p1 = date.split("=")[1]
    if userID == int(p1):
      start = """👋🏻꒐ ❌⭕️
👤꒐ اضغط للعب مع ({})""".format(userFN)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton("العب", callback_data="xo="+str(userID))]])
      Bot("sendMessage",{"chat_id":chatID,"text":start,"disable_web_page_preview":True,"reply_markup":kb})
      Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":tx,"disable_web_page_preview":True})
    else:
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"عذراً اللعبه ليست لك","show_alert":True})


  if re.search("^xo.pyplay$",date):
    start = """👋🏻꒐ ❌⭕️
👤꒐ اضغط للعب مع ({})""".format(userFN)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("العب", callback_data="xo="+str(userID))]])
    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":start,"disable_web_page_preview":True,"reply_markup":kb})


  if re.search("xo=",date):
    p1 = date.split("=")[1]
    if userID == int(p1):
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"انت من بدأت اللعبه انتظر احد اصدقائك","show_alert":True})
      return False
    
    try:
      getUser = client.get_users(p1)
      fn1 = getUser.first_name
    except Exception as e:
      fn1 = p1
    p2 = userID
    fn2 = userFN
    tb = [0,0,0,0,0,0,0,0,0]
    cd = "xp{}={}={}={}".format(1,p1,p2,tb)
    i = 0
    x = 0
    ar = []
    a = []
    em = "◻️"

    while i < 3:
      while x < 3:
        cd = "xp{}={}={}={}={}.{}".format(1,p1,p2,tb,i,x)
        a.append(InlineKeyboardButton(em,callback_data=cd))
        x += 1
      i += 1
      x = 0
      ar.append(a)
      a = []
    ar.append([InlineKeyboardButton("📣",url="t.me/zx_xx")])
    kb = InlineKeyboardMarkup(ar)
    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go.format("👉🏻",fn1,"🔄",fn2),"disable_web_page_preview":True,"reply_markup":kb})

  if re.search("xp(1|2)=",date):
    play = date.split("=")[0].replace("xp","")
    p1 = date.split("=")[1]
    p2 = date.split("=")[2]
    ck = date.split("=")[3]
    rt = date.split("=")[4]
    r = rt.split(".")[0]
    t = rt.split(".")[1]
    if int(play) == 1:
      playing = p1
      nextT = p2
      nextTN = 2
      xo = 1#"X"
      em = "❌"
    elif int(play) == 2:
      playing = p2
      xo = 2#"O"
      nextT = p1
      nextTN = 1
      em = "⭕️"

    if userID != int(playing):
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"انتظر دورك","show_alert":True})
      return False
    x = 0
    a =[]
    ar = []
    for i in json.loads(ck):
      a.append(i)
      x += 1
      if x == 3:
        x = 0
        ar.append(a)
        a = []
    tx = callback_query.message.reply_markup.inline_keyboard
    if ar[int(r)][int(t)] == 0:
      ar[int(r)][int(t)] = xo
    else:
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"لايمكنك اللعب هنا","show_alert":True})
      return False
    tb = ar[0] + ar[1] + ar[2]
    win,xRo = getwin(tb)
    
    if win:
      if xRo == 1:
        fn1,fn2 = get(client,userID,userFN,p1,p2)
        redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),p1,10)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("اللعب مجدداً",callback_data="rex={}".format(p1))]])
        Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go3.format("❌",fn1,"⭕️",fn2,fn1)+"\n"+kbtotx(tb),"disable_web_page_preview":True,"reply_markup":kb})
        return False
      if xRo == 2:
        fn1,fn2 = get(client,userID,userFN,p1,p2)
        redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),p2,10)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("اللعب مجدداً",callback_data="rex={}".format(p1))]])
        Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go3.format("❌",fn1,"⭕️",fn2,fn2)+"\n"+kbtotx(tb),"disable_web_page_preview":True,"reply_markup":kb})
        return False
    if xRo == "tie":
      fn1,fn2 = get(client,userID,userFN,p1,p2)
      redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),p1,3)
      redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),p2,3)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton("اللعب مجدداً",callback_data="rex={}".format(p1))]])
      Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go2.format("❌",fn1,"⭕️",fn2)+"\n"+kbtotx(tb),"disable_web_page_preview":True,"reply_markup":kb})
      return False
    
    win = getwin(tb)
    i = 0
    x = 0
    ar = []
    a = []
    while i < 3:
      while x < 3:
        cd = "xp{}={}={}={}={}.{}".format(nextTN,p1,p2,tb,i,x)
        if int(r) == i and int(t) == x:
          a.append(InlineKeyboardButton(em,callback_data=cd))
        else:
          a.append(InlineKeyboardButton(tx[i][x].text,callback_data=cd))
        x += 1
      i += 1
      x = 0
      ar.append(a)
      a = []
    ar.append([InlineKeyboardButton("📣",url="t.me/zx_xx")])
    kb = InlineKeyboardMarkup(ar)
    if nextTN == 1:
      e1 = "👉🏻"
    else:
      e1 = "🔄"
    if nextTN == 2:
      e2 = "👉🏻"
    else:
      e2 = "🔄"
    fn1,fn2 = get(client,userID,userFN,p1,p2)
    v= Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go.format(e1,fn1,e2,fn2),"disable_web_page_preview":True,"reply_markup":kb})

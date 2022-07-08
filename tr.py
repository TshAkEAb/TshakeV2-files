from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib
def updateMsgs(client, message,redis):
    type = message.chat.type
    userID = message.from_user.id
    chatID = message.chat.id
    rank = isrank(redis,userID,chatID)
    text = message.text
    title = message.chat.title
    userFN = message.from_user.first_name
    type = message.chat.type

    if text and text == "نقل البيانات" and rank == "sudo" and message.reply_to_message.document:
        msgID = Bot("sendMessage",{"chat_id":chatID,"text":"انتظر قليلاً يتم تحميل الملف ℹ️","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})["result"]["message_id"]

        fileName = message.reply_to_message.download()
        JsonDate = json.load(open(fileName))
        if int(JsonDate["BOT_ID"]) != int(BOT_ID):
            Bot("editMessageText",{"chat_id":chatID,"text":"عذراً هذه الملف ليس لي ⚠️","message_id":msgID,"disable_web_page_preview":True,"parse_mode":"html"})
            return 0
        co = len(JsonDate["GP_BOT"])
        Bot("editMessageText",{"chat_id":chatID,"text":f"تم ايجاد {co} مجموعه في الملف ℹ️","message_id":msgID,"disable_web_page_preview":True,"parse_mode":"html"})
        for chatID in JsonDate["GP_BOT"].keys():
            try:
                time.sleep(0.1)
                print(chatID)
                Bot("exportChatInviteLink",{"chat_id":chatID})
                add = redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
                locksarray = {'Llink','Llongtext','Lmarkdown','Linline','Lfiles','Lcontact','Lbots','Lfwd','Lnote'}
                for lock in locksarray:
                    redis.sadd("{}Nbot:{}".format(BOT_ID,lock),chatID)
                ads = Bot("getChatAdministrators",{"chat_id":chatID})
                for ad in ads['result']:
                    userId = ad["user"]["id"]
                    userFn = ad["user"]["first_name"]
                    if ad['status'] == "administrator" and int(userId) != int(BOT_ID):
                        setrank(redis,"admin",userId,chatID,"array")
                    if ad['status'] == "creator":
                        setrank(redis,"malk",userId,chatID,"one")
                gpDate = JsonDate["GP_BOT"][chatID]
                if "ASAS" in gpDate:
                    for userId in gpDate["ASAS"]:
                        setrank(redis,"acreator",userId,chatID,"array")
                if "MNSH" in gpDate:
                    for userId in gpDate["MNSH"]:
                        setrank(redis,"creator",userId,chatID,"array")
                if "MDER" in gpDate:
                    for userId in gpDate["MDER"]:
                        setrank(redis,"owner",userId,chatID,"array")
                if "MOD" in gpDate:
                    for userId in gpDate["MOD"]:
                        setrank(redis,"admin",userId,chatID,"array")
            except Exception as e:
                print(e)
        Bot("editMessageText",{"chat_id":chatID,"text":f"تم نقل المجموعات ✅","message_id":msgID,"disable_web_page_preview":True,"parse_mode":"html"})

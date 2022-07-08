from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from uuid import uuid4

from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)


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
    words = ["سحور","سياره","استقبال","قنفه","ايفون","بزونه","مطبخ","كرستيانو","دجاجه","مدرسه","الوان","غرفه","ثلاجه","كهوه","سفينه","العراق","محطه","طياره","رادار","منزل","مستشفى","كهرباء","تفاحه","اخطبوط","سلمون","فرنسا","برتقاله","تفاح","مطرقه","بتيته","لهانه","شباك","باص","سمكه","ذباب","تلفاز","حاسوب","انترنيت","ساحه","جسر","باي","فهمت","موزين","اسمعك","احبك","موحلو","نضيف","حاره","ناصي","جوه","سريع","ونسه","طويل","سمين","ضعيف","شريف","شجاع","رحت","عدل","نشيط","شبعان","موعطشان","خوش ولد","اني","هادئ"]
    emoje = ["😸","☠️","🐼","🐇","🌑","🌚","⭐️","✨","⛈","🌥","⛄️","👨‍🔬","👨‍💻","👨‍🔧","🧚‍♀️","🧜‍♂️","🧝‍♂️","🙍‍♂️","🧖‍♂️","👬","🕒","🕤","⌛️","📅",]
    
    if text and re.search("^الاسرع$",text) and not redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID):
        word = random.choice(words)
        print(word)
        word_list = list(word)
        random.shuffle(word_list)
        W = " ".join(word_list)
        Bot("sendMessage",{"chat_id":chatID,"text":f"⏺꒐ الاحرف : {W}\nارسل الكلمه بالرد","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
        redis.hset("{}Nbot:fastest".format(BOT_ID),chatID,word)

    if text and re.search("^العكس$",text) and not redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID):
        word = random.choice(words)
        reversed_word = word [::-1]
        Bot("sendMessage",{"chat_id":chatID,"text":f"⏺꒐ الكلمه : {reversed_word}\nارسل الكلمه بالرد","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
        redis.hset("{}Nbot:reversed".format(BOT_ID),chatID,word)

    if text and re.search("^المختلف$",text) and not redis.sismember("{}Nbot:gpgames".format(BOT_ID),chatID):
        emoje_1 = random.choice(emoje)
        emoje.remove(emoje_1)
        emoje_2 = random.choice(emoje)
        array = [emoje_1]
        for i in range(7):
           array.append(emoje_2)
        random.shuffle(array)
        E = "".join(array)
        Bot("sendMessage",{"chat_id":chatID,"text":f"⏺꒐ {E}\nارسل الايموجي بالرد","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
        redis.hset("{}Nbot:different".format(BOT_ID),chatID,emoje_1)


    if message.reply_to_message:
        if message.reply_to_message.from_user:
            if text and message.reply_to_message.from_user.id == int(BOT_ID) and text == redis.hget("{}Nbot:fastest".format(BOT_ID),chatID) :
                Bot("sendMessage",{"chat_id":chatID,"text":f"🎉꒐ مبروك لقد فزت","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
                redis.hdel("{}Nbot:fastest".format(BOT_ID),chatID)
            if text and message.reply_to_message.from_user.id == int(BOT_ID) and text == redis.hget("{}Nbot:reversed".format(BOT_ID),chatID) :
                Bot("sendMessage",{"chat_id":chatID,"text":f"🎉꒐ مبروك لقد فزت","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
                redis.hdel("{}Nbot:reversed".format(BOT_ID),chatID)
            if text and message.reply_to_message.from_user.id == int(BOT_ID) and text == redis.hget("{}Nbot:different".format(BOT_ID),chatID) :
                Bot("sendMessage",{"chat_id":chatID,"text":f"🎉꒐ مبروك لقد فزت","reply_to_message_id":message.id,"parse_mode":"html","disable_web_page_preview":True})
                redis.hdel("{}Nbot:different".format(BOT_ID),chatID)

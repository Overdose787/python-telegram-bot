import asyncio , telegram 

import telegram.ext as tge

import data

import logging , json , random

import ffparser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
token = data.data.token

chatid = data.data.chatid
"""
app = tge.ApplicationBuilder()
app.token(token)
app.build()
"""

app = tge.ApplicationBuilder().token(token).build()

tracked_msg = []

async def sec_check(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE , effective_id):
    if effective_id != chatid:
        await context.bot.send_message(
                text="Authentication failure error \n most likely you are trying to acces the bot outside permitted chat \n please contact the developer for further help",
                chat_id=effective_id)
        return False
    return True

def addthing(itext , name):
    async def handlemassage(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
        if await sec_check(update , context , update.effective_chat.id):
            tracked_msg.append(update.effective_message.id)
            msg = await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=itext)
            tracked_msg.append(msg.message_id)

    starthandler = tge.CommandHandler(name , handlemassage)
    app.add_handler(starthandler)

addthing("Привіт! я - АСГІ 👋, Автоматизована система групових інтеракцій , моя задача забезпечети зручну систему опитуваннь в 1 клік! , взагалі то я просто побочний проект людини юку ви всі знаєте , я покищо мало що вмію , але коли в мене з'явиться краще тіло я зможу хостити вам ігри🤗 , також чим можу похвалитись навідмінок він ярікового блядьского зазивали , в мене є функція , щоб можна було вийти з пула тегів , та я вас не турбувала❤️" , "tbu")
addthing(ffparser.fasff() , "ff")

async def autocleanup(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        tracked_msg.append(update.effective_message.id)
        await context.bot.deleteMessages(chat_id=update.effective_chat.id,message_ids=tracked_msg)
        tracked_msg.clear()

async def call(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        parsed=""
        tracked_msg.append(update.effective_message.id)
        with open("friend.json" , "r" , encoding="utf-8") as f:
             friends = json.load(f)
        with open("popular_emojis.txt" , "r") as f:
             emj = f.read()
             emj.splitlines()
        for items in friends.values():
            rc = random.choice(emj)
            parsed += f"@{items} {rc}"
        msg = await context.bot.send_message(text=parsed , chat_id=update.effective_chat.id)
        tracked_msg.append(msg.id)

async def checkopt(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        tracked_msg.append(update.effective_message.id)
        with open("friend.json" , "r", encoding="utf-8") as frj:
            friends = json.load(frj)
        for key in friends:
            if int(key) == update.effective_sender.id:       
                msg = await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Ви є в базі данних 😊")
                tracked_msg.append(msg.message_id)
                friends.clear()
                return 0
        msg = await context.bot.send_message(
             chat_id=update.effective_chat.id,
             text="Вас немає в базі даних🤔")
        friends.clear()
        tracked_msg.append(msg.message_id)
        return 1

async def optin(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        if await checkopt(update , context) == 1:
            msg = await context.bot.send_message(text="Додаю 😄" ,chat_id=chatid)
            tracked_msg.append(msg.id)
            with open("friend.json" , "r" , encoding="utf-8") as f:
               friends = json.load(f)
               friends[update.effective_sender.id] = update.effective_sender.username
            with open("friend.json" , "w" , encoding="utf-8") as f:
                json.dump(friends ,f)
                friends.clear()
            await checkopt(update , context)

async def optout(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        if await checkopt(update,context) == 0:
            msg = await context.bot.send_message(text = "Видаляю 🤗" , chat_id=chatid)
            tracked_msg.append(msg.id)
            with open("friend.json" , "r" , encoding="utf-8") as f:
                friends = json.load(f)
                friends.pop(str(update.effective_sender.id))
            with open("friend.json" , "w" , encoding="utf-8") as f:
                json.dump(friends , f)
                friends.clear()
            await checkopt(update , context)

async def poll(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await sec_check(update , context , update.effective_chat.id):
        await call(update , context)
        msg = await context.bot.send_poll(chat_id=chatid , question="Хто грать? 📢📢📢" , options=["+","-"])
        tracked_msg.append(msg.id)

app.add_handler(tge.CommandHandler("co" , checkopt))
app.add_handler(tge.CommandHandler("ac" , autocleanup))
app.add_handler(tge.CommandHandler("oi" , optin))
app.add_handler(tge.CommandHandler("ou" , optout))
app.add_handler(tge.CommandHandler("call", call))
app.add_handler(tge.CommandHandler("poll",poll))

app.run_polling()

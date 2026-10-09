import asyncio , telegram 

import telegram.ext as tge

import data

import logging , json

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

def addthing(itext , name):
    async def handlemassage(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):

        if update.effective_chat.id == chatid:
            tracked_msg.append(update.effective_message.id)

            
            msg = await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=itext)

            tracked_msg.append(msg.message_id)
                    
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Authentication failure error \n most likely you are trying to acces the bot outside permitted chat \n please contact the developer for further help")

    starthandler = tge.CommandHandler(name , handlemassage)
    app.add_handler(starthandler)

addthing("Привіт! я - АСГІ 👋, Автоматизована система групових інтеракцій , моя задача забезпечети зручну систему опитуваннь в 1 клік! , взагалі то я просто побочний проект людини юку ви всі знаєте , я покищо мало що вмію , але коли в мене з'явиться краще тіло я зможу хостити вам ігри🤗 , також чим можу похвалитись навідмінок він ярікового блядьского зазивали , в мене є функція , щоб можна було вийти з пула тегів , та я вас не турбувала❤️" , "tbu")
addthing(ffparser.fasff() , "ff")

async def autocleanup(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    tracked_msg.append(update.effective_message.id)
    await context.bot.deleteMessages(chat_id=chatid,message_ids=tracked_msg)
    tracked_msg.clear()
'''
async def call(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    tracked_msg.append(update.effective_message.id)
    await context.bot.
'''
async def checkopt(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    tracked_msg.append(update.effective_message.id)
    with open("friend.json" , "r", encoding="utf-8") as frj:
        friends = json.load(frj)
    for key in friends:
        if int(key) == update.effective_sender.id:       
            msg = await context.bot.send_message(
                     chat_id=chatid,
                     text="Ви є в базі данних 😊")
            tracked_msg.append(msg.message_id)
            friends.clear()
            return 0
    msg = await context.bot.send_message(
            chat_id=chatid,
            text="Вас немає в базі даних🤔"
            )
    friends.clear()
    tracked_msg.append(msg.message_id)
    return 1

async def optin(update: telegram.Update , context: tge.ContextTypes.DEFAULT_TYPE):
    if await checkopt(update , context) == 1:
        msg = await context.bot.send_message(text="Додаю 😄" ,chat_id=chatid)
        tracked_msg = msg.id
        with open("friend.json" , "r" , encoding="utf-8") as f:
            friends = json.load(f)
            friends[update.effective_sender.id] = update.effective_sender.username
        with open("friend.json" , "w" , encoding="utf-8") as f:
            json.dump(friends ,f)
            friends.clear()
        await checkopt(update , context)


app.add_handler(tge.CommandHandler("co" , checkopt))
app.add_handler(tge.CommandHandler("ac" , autocleanup))
app.add_handler(tge.CommandHandler("oi" , optin))

app.run_polling()

import asyncio , telegram , telegram.ext , time , data

async def delall(dct, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    keylist = []
    for key in dct.keys():
        await context.bot.delete_message(data.data.chatid, key)
        keylist.append(key)
    for items in keylist:
        dct.pop(items)

def addmsg(id,dct):
    dct[id]=0


async def live_msg(dct,context: telegram.ext.ContextTypes.DEFAULT_TYPE, delete_from = 45 , remove_after = 47):

     while True:
        print("starting routine message checkup")
        oldtime = int(time.strftime("%H" , time.localtime()))

        await asyncio.sleep(900)
        
        if len(dct) == 0:
            print("nothing to check up , skipping")
            continue

        total = int(time.strftime("%H" , time.localtime())) - oldtime

        if total != 0:
            keylist = []
            print(dct)
            for key , value in dct.items():
                dct[key] = value + 1
                if value >= delete_from and value < remove_after:
                    await context.bot.delete_message(chat_id=data.data.chatid , message_id=key)
                    keylist.append(key)
                elif value >= remove_after:
                    print(f"WARNING!!! DELETING {key} EXCEPRION ARISEN value - {value}")
                    keylist.append(key)
            if len(keylist) != 0:
                for items in keylist:
                    dct.pop(items)
        print("finished")

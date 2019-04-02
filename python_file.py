from telegram.ext import Filters, CommandHandler, MessageHandler, Updater
from telegram import ChatAction
from gtts import gTTS
import pymysql

def start(bot, update):
    update.message.reply_text("Bot started. The use of this bot is related to his physical machine.")
    from sys import argv
    fp = argv[1]
    txt = open(fp)
    for strng in txt.read().splitlines():
        task.append(strng)
    txt.close()

def echo(bot, update):
    update.message.reply_text("This bot accepts only commands. Messages will be ignored.")

def showTask(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    sql= "SELECT * FROM task_list.tasks"
    conn= pymysql.connect(user='root', password='user', host='localhost', database='task_list')
    cur= conn.cursor()
    cur.execute(sql)
    res=[]
    for i in cur.fetchall():
        res.append(i[1])
    if(len(res)<=0):
        update.message.reply_text("No tasks in memory. Nothing to do now.")
    else:
        l2 = list(res)
        update.message.reply_text(sorted(l2))
        del l2[:]
    cur.close()
    conn.close()

def newTask(bot, update, args):
    sql = "INSERT INTO task_list.tasks(todo) VALUES (%s)"
    conn = pymysql.connect(user='root', password='user', host='localhost', database='task_list')
    cur = conn.cursor()
    strng = ""
    i = 0
    for s in args:
        strng = strng + s
        if i != (len(args) - 1):
            strng += " "
        i += 1
    cur.execute(sql, (strng, ))
    conn.commit()
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text(strng+"\n"+"-INSERTED-")
    cur.close()
    conn.close()


    task.append(strng)

def removeTask(bot, update, args):
    sql = "DELETE FROM task_list.tasks WHERE todo= (%s)"
    conn = pymysql.connect(user='root', password='user', host='localhost', database='task_list')
    cur = conn.cursor()
    sql_check= "SELECT * FROM task_list.tasks"
    cur.execute(sql_check)
    if(cur.rowcount==0):
        update.message.reply_text("No tasks in memory. Nothing to do now.")
    else:
        strng = ""
        i= 0
        for s in args:
            strng = strng + s
            if i!= (len(args)-1):
                strng+= " "
            i+=1
        cur.execute(sql, (strng,))
        conn.commit()
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text(strng + "\n" + "-DELETED-")
    cur.close()
    conn.close()

def removeAllTasks(bot, update, args):
    sql = "DELETE FROM task_list.tasks WHERE todo like (%s)"
    conn = pymysql.connect(user='root', password='user', host='localhost', database='task_list')
    cur = conn.cursor()
    sql_check = "SELECT * FROM task_list.tasks"
    cur.execute(sql_check)
    if (cur.rowcount == 0):
        update.message.reply_text("No tasks in memory. Nothing to do now.")
    else:
        strng = ""
        i = 0
        for s in args:
            strng = strng + s
            if i != (len(args) - 1):
                strng += " "
            i += 1
        cur.execute(sql, ("%"+strng+"%",))
        conn.commit()
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text(strng + "\n" + "-DELETED-")
    cur.close()
    conn.close()

def main():
    bot_updater= Updater("633860381:AAE4lOKbl5w4JpUGeYW9WMMMM2vn2rZuyxM") #collegamento al bot
    bot_dispatcher= bot_updater.dispatcher #registro degli handler

    bot_dispatcher.add_handler(CommandHandler("start", start))
    bot_dispatcher.add_handler(MessageHandler(Filters.text, echo))
    bot_dispatcher.add_handler(CommandHandler("showtask", showTask))
    bot_dispatcher.add_handler(CommandHandler("newtask", newTask, pass_args=True))
    bot_dispatcher.add_handler(CommandHandler("removetask", removeTask, pass_args=True))
    bot_dispatcher.add_handler(CommandHandler("removealltasks", removeAllTasks, pass_args=True))

    bot_updater.start_polling() #start the bot itself

    bot_updater.idle() #run the bot until the user press CTRL+C (sending a SIGINT, SIGABRT, ...) stopping the bot

if (__name__ == "__main__"):
    task = []
    main()
# -*- coding: utf-8 -*-
"""
This is a detailed example using almost every command of the API
"""
import feedparser
import telebot
from telebot import types
import time

TOKEN = 'TOKEN_NEWS'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  
                'news': 'Get the latest news',
              'help': 'Gives you information about the available commands'
              
}

rss_news = {
                "ideal": {
                            "url":"http://www.ideal.es/granada/rss/atom/portada#ns_campaign=rss&ns_mchannel=rss-atom&ns_source=portada&ns_linkname=test&ns_fee=0",
                            "title": True,
                            "summary": True,
                            "link": True
                        },
                "elmundo": {
                            "url": "http://estaticos.elmundo.es/elmundo/rss/andalucia.xml",
                            "title": True,
                            "summary": False,
                            "link": True
                        }, 
            }


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0


def send_news(cid, text="ideal", count=0, limit=10):
    python_wiki_rss = rss_news[text]
    feed = feedparser.parse(python_wiki_rss["url"])

    #print feed.entries

    for entrie in feed.entries:
        if(count==limit):
            break

        title = u"🗞 %s 🗞\n\n" % (entrie.title) if python_wiki_rss["title"] else ""
        summary = u"%s \n" % (entrie.summary) if python_wiki_rss["summary"] else ""
        link = u"%s" % (entrie.link) if python_wiki_rss["link"] else ""

        bot.send_message(cid, u"%s%s%s" % (title, summary, link))
        count+=1

    print "holaa"

    
def newspapers():
    newspaper = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    for key in rss_news:
        newspaper.add(key)
    hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard

    return newspaper


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print u"" + (m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text
            

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page
    

@bot.message_handler(commands=['news'])
def command_news(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your news now", reply_markup=newspapers())  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_news_select(m):
    cid = m.chat.id
    text = m.text
    
    send_news(cid, text)

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()
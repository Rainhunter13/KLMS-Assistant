# import other files used
import portal   # for checking correctness of username and password
import klms_notice  # for last notices function

# import required libraries
import telebot
import time
import requests
from bs4 import BeautifulSoup

# from telegram.ext.dispatcher import run_async

# declaring global variables

                    # dictionaries of:
username = {}           # username of user
password = {}           # password of user
uses = {}               # 1 if user started the bot
c = {}                  # number of requests for checking new notices
stop = {}               # 1 when stopping pushing notices, 0 otherwise
notices_id = {}         # list of notices ids

# bot unique token
bot = telebot.TeleBot('949830455:AAHRHRJQsOjqzOVvIVYxFNDCnesmnQSTgz4')

# Identifying keyboards for short answers
TrueFalseKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
TrueFalseKeyboard.row("Correct", "Retype")
YesNoKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
YesNoKeyboard.row("YES", "NO")

# Commands

# @run_async
# start contacting with bot
@bot.message_handler(commands=['start'])
def start_message(message):
    global uses
    global c
    global stop
    global notices_id
    global username
    global password
    bot.send_message(message.chat.id, 'Hi, my name is KLMS Assistant. I can help you to using KLMS service. If you want to use me, choose "YES".\n\n', reply_markup = YesNoKeyboard)
    uses[message.chat.id] = 1
    c[message.chat.id] = 0
    stop[message.chat.id] = 0
    notices_id[message.chat.id] = []
    username[message.chat.id] = ""
    password[message.chat.id] = ""

# @run_async
# stop pushing notices
@bot.message_handler(commands=['stop_notices'])
def stop_notices(message):
    global stop
    bot.send_message(message.chat.id, "Notifications were turned off.")
    stop[message.chat.id] = 1

# @run_async
# list of possible commands
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "List of commands:\n/start - start/restart contacting with bot\n/last_notices - last notices from your account KLMS\n/set_notices - set bot to notify you for new KLMS notices\n/stop_notices - stop receiving notifications from bot\n/help - list of possible commands")

# @run_async
# list of last notices
@bot.message_handler(commands=['last_notices'])
def last_notices(message):
    global username
    global password
    bot.send_message(message.chat.id, "Please, wait 10 seconds.")
    while True:
        try:
            bot.send_message(message.chat.id, klms_notice.notices(username[message.chat.id], password[message.chat.id]))
        except:
            continue
        else:
            break

# @run_async
# setting pushing notices
@bot.message_handler(commands=['set_notices'])
def set_notices(message):
    global username
    global password
    global stop
    global c
    global notices_id
    bot.send_message(message.chat.id, "Starting from now, I will notify you if there will be a new notice on KLMS.")
    stop[message.chat.id] = 0
    c[message.chat.id] = 0
    notices_id[message.chat.id] = []
    notify_always(username[message.chat.id], password[message.chat.id], message.chat.id)

# @run_async
# message reply
@bot.message_handler(content_types=['text'])
def send_text(message):
    global username
    global password
    if message.text.lower() == "yes":
        bot.send_message(message.chat.id, "To continue, I will need your account to KLMS. For our part, we guarantee that any your private information isn't used for any reasons except the primary purpose of this bot and never given to the third parties (even to the bot creator).\nPlease, enter login and password in format:\nusername password")
        bot.register_next_step_handler(message, callback = read_account)
    elif message.text.lower() == "no":
        bot.send_message(message.chat.id, "Ok :(\nHope you will use me later. See you.")
    elif message.text.lower() == "retype":
        bot.send_message(message.chat.id, "Please, type in format:\nusername password")
        bot.register_next_step_handler(message, callback = read_account)
    elif message.text.lower() == "correct":
        bot.send_message(message.chat.id, "Checking account details..")
        t = check_password(username[message.chat.id], password[message.chat.id], message.chat.id)
        if t==1:
            bot.send_message(message.chat.id, "Congrulations, everything is set up! To see the list of possible commands, write '/help'")
        else:
            bot.send_message(message.chat.id, "You entered invalid username or password, write 'retype' to enter again.")
    else:
        bot.send_message(message.chat.id, "Sorry, but I can't understand you. To see the list of possible commands write '/help'")

# parse username and password from a message
def read_account(message):
    a = message.text.split()
    global username
    global password
    if len(a) != 2:
        bot.send_message(message.chat.id, "Please, type in format:\nusername password")
        bot.register_next_step_handler(message, callback = read_account)
        return
    username[message.chat.id] = a[0]
    password[message.chat.id] = a[1]
    bot.send_message(message.chat.id, "Please, check the details: (type or choose 'Correct'/'Retype')")
    bot.send_message(message.chat.id, "username: " + username[message.chat.id])
    bot.send_message(message.chat.id, "password: " + password[message.chat.id], reply_markup = TrueFalseKeyboard)

# check entered username and password for correctness
# actually, checks if access to KAIST Portal  access was done successfully, i.e. we can parse data(news) from it
def check_password(username, password, id):
    try:
        a = portal.portal_login(username, password)
        if len(a) < 30:
            return 0
        return 1
    except:
        bot.send_message(id, "Connection error occured, please retype 'Correct'.")

# helper method for set_notices
def notify_always(username, password, id):
    global c
    global stop
    while stop[id] == 0:
        try:
            a = check_and_notify(username, password, id)
            if c[id] > 0:
                if len(a) > 29:
                    bot.send_message(id, a)
                else:
                    # pass
                    bot.send_message(id, "There are no new notices yet")
            else:
                c[id] = c[id] + 1
        except:
            continue
        else:
            time.sleep(60)

# main requests for new notices
def check_and_notify(username, password, id):
    global notices_id

    r = requests.Session()

    headersPost = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://ksso.kaist.ac.kr/iamps/IntegratedLogin.do",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    data = {
        "refererUrl": "https://klms.kaist.ac.kr/login.php",
        "message": "",
        "userSe": "USR",
        "j_username": "",
        "id": username,
        "password": password
    }

    headersGet = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://ksso.kaist.ac.kr/iamps/IntegratedAuth.do',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://klms.kaist.ac.kr/login.php',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    r.get("https://ksso.kaist.ac.kr/iamps/requestLogin.do", headers = headers1)
    time.sleep(1)
    r.post(url="https://ksso.kaist.ac.kr/iamps/IntegratedAuth.do", headers=headersPost, data=data)
    time.sleep(1)
    text = r.get('http://klms.kaist.ac.kr/', headers=headersGet)

    soup = BeautifulSoup(text.text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    notice = soup.find(attrs = {'class' : 'notification_list'})
    notices1 = notice.find_all('a')
    notices2 = notices1

    s = "You have a new notice(s)!\n\n"

    for i in range(len(notices1)):
        last_id = notices1[i]['href'][notices1[i]['href'].find('id')+3:notices1[i]['href'].find('id')+9];
        if (not last_id  in notices_id[id]):
            notices_id[id].append(last_id)
            if (notices1[i].img == None):
                s1 = notices1[i].find('h5')
                s2 = notices2[i].find('p')
                s2.span.decompose()
                s = s + s1.string + ":\n" + s2.string + "\n"
            else:
                s1 = notices1[i]
                s1.img.decompose()
                s1 = s1.find('h5')
                s2 = notices2[i].find('p')
                if (s1.img != None):
                    s1.img.decompose()
                s2.span.decompose()
                s = s + s1.string + ":\n" + s2.string + "\n"

    return s

bot.polling()
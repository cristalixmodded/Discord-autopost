import json
import discum
import time
from datetime import datetime, timedelta
import random
import configparser
from plyer import notification
import pytz

config = configparser.ConfigParser()
config.read_file(open(r'config.ini'))
discord_token = config.get('Config', 'discord_token')
warp_name = config.get('Config', 'warp_name')
delay = config.get('Config', 'delay') * 60
MIN_delay = config.get('Config', 'MIN_delay') * 60
MAX_delay = config.get('Config', 'MAX_delay') * 60
channel_ID = config.get('Config', 'channel_ID')
message_content = config.get('Config', 'message_content')

delete_message = eval(config.get('Config', 'delete_message'))
random_time = eval(config.get('Config', 'random_time'))
notifications = eval(config.get('Config', 'notifications'))

bot = discum.Client(token=discord_token)

def send():
    last_message_id = None
    while True:
        messages = bot.getMessages(channelID=channel_ID, num=100, beforeDate=last_message_id)
        messages = messages.text
        messages = messages.replace('\\n', '')
        messages = messages.replace('\\"', '')
        messages = messages.encode().decode("unicode-escape")
        messages = messages.replace('\\', '')

        messages = json.loads(messages)

        message_founded = False
        for j in messages:
            if not message_founded:
                if j['author'].get('id') == '618536577282342912':
                    content = j['content']
                    for wn in warp_name:
                        if ' '+wn in content:
                            pos = content.find(' '+wn)
                            if pos+len(wn)+1 < len(content):
                                if not content[pos+len(wn)+1].isalnum():
                                    message_founded = True
                                    message_timestamp = j['content'][1:20]
                            else:
                                message_founded = True
                                message_timestamp = j['content'][1:20]
            last_message_id = j['id']

        if message_founded:
            message_founded = False
            last_message_id = None

            message_time = datetime.strptime(message_timestamp, '%d.%m.%Y %H:%M:%S')
            timezone = pytz.timezone('Europe/Moscow')
            now = datetime.now(timezone)

            if message_time < now - timedelta(minutes=10):
                sended_message = bot.sendMessage(channelID=channel_ID, message=message_content)
                sended_message = sended_message.text.encode().decode('unicode-escape')
                
                if notifications:
                    local_time = datetime.now()
                    local_time = local_time.strftime("%d/%m/%Y %H:%M:%S")
                
                    notification.notify(title="Сообщение отправлено.", message=str(local_time))
                if delete_message:
                    sended_message_json = json.loads(sended_message.replace('\\', ''))
                    bot.deleteMessage(channelID=channel_ID, messageID=sended_message_json['id'])
                time.sleep(600)
            else:
                wait = message_time - now + timedelta(minutes=10)
                time.sleep(wait.total_seconds())

            if random_time:
                time.sleep(random.randint(MIN_delay, MAX_delay))
            else:
                time.sleep(delay)

        else:
            time.sleep(1)
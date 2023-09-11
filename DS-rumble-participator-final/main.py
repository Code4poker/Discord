import requests as r
import time
import json
import datetime
from datetime import datetime
import threading


delay = 1
thread_list = []

# get info from json file
def loadInfo():
    with open('info.json', 'r') as f:
        return json.load(f)


# parse messages
def getMessages(acc_info, chat_id, limit):
    s = acc_info['session']
    print(type(s))
    resp = s.get(
        f'https://discord.com/api/v9/channels/{chat_id}/messages?limit={limit}'
    )
    return resp.json()


def postReaction(acc_info, chat_id, message_id):
    s = acc_info['session']
    print(type(s))
    url = f'https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}/reactions/Sw0rds%3A975453286222155786/%40me?location=Message'
    s.put(url)


# monitor new posts
def monitorRumble(acc_info):
    key_string = 'Click the emoji below to join'
    account_name = acc_info['name']
    entered_rumbles = []
    
    while True:

        try:
            for chat_id in acc_info['chat_ids']:
            
                last_messages = getMessages(acc_info, chat_id, 100) # last msg with index 0
                
                for message in last_messages:
                    if message['author']['id'] == acc_info['bot_id']:
                        if message['id'] not in entered_rumbles:
                            embed = message['embeds'][0]
                            
                            if key_string in embed['description']:
                                postReaction(acc_info, chat_id, message['id'])
                                entered_rumbles.append(message['id'])
                                print(f'{datetime.now()} - {account_name} - entered rumble')

                time.sleep(delay)
                    
            time.sleep(delay)
        except:
            print('Unknown error')

if __name__ == '__main__':
    # get info from json file
    info = loadInfo()

    i = 0


    for account in info['accounts']:
        s = r.Session()
        s.headers = info['accounts'][i]['headers']
        s.proxies = info['accounts'][i]['proxies']
        info['accounts'][i]['session'] = s

        acc_info = info['accounts'][i]
        t = threading.Thread(target=monitorRumble, args = (acc_info,))
        thread_list.append(t)
        i += 1

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


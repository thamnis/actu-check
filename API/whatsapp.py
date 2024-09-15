from pathlib import Path
import json
from twilio.rest import Client

with open((Path().cwd() / 'keys' / 'twilio.json'), 'r') as f:
    k = json.load(f)
    account_sid = k['account_sid']
    auth_token = k['auth_token']
    sender = k['sender']

client = Client(account_sid, auth_token)


def send_whatsapp(filepath, receiver):
    with open(filepath, 'r', encoding='utf-8') as f2:
        j = json.load(f2)
        for i in range(len(j)):
            title = j[str(i)]['title']
            url = j[str(i)]['url']
            prev = j[str(i)]['prev']
            topic = j[str(i)]['topic']
            date = j[str(i)]['date']

            # print(message)

            message = client.messages.create(
                from_=sender,
                media_url=prev,
                body=f'*{title}*\n{topic[:500]}...\n{url}\n{date}',
                to=receiver
            )

            print(message.sid)

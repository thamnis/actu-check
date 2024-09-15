from pathlib import Path
from API.whatsapp import send_whatsapp
from API.ivoirbusiness import get_ivoirebusiness

with open(Path().cwd() / 'files' / 'receivers.csv', 'r') as f:
    for receiver in f.read().split(','):
        send_whatsapp(get_ivoirebusiness(), receiver)

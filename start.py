from os import system as bash
bash('pip3 install -r requirements.txt')
bash('python3 bot.py & python3 keepalive.py')

from os import system as bash
bash('pip3 install -r reqs.txt')
bash('ruby ext/setup.rb & ruby ext/addons/mail.rb ext/data/mail/spool & python3 bot.py & python3 keepalive.py')


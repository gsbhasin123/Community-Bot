from os import system as bash
import threading
bash('pip3 install -r reqs.txt')
def ruby():
    bash('ruby ./ext/ruby/setup.rb')
threading.Thread(target=ruby)
bash('python3 bot.py & python3 keepalive.py')


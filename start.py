from os import system as bash
modules = ['flask','sqlalchemy','youtube-dl','leonardo-team','utils','xiangcheck']
for module in modules:
    bash(f'pip3 install {module}')
bash('python3 keepalive.py & python3 bot.py')

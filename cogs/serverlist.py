from hata import ChannelText, eventlist, Embed
from hata.events import Pagination

CENTRAL_CHANNEL = ChannelText.precreate(640258344531001354)

commands = eventlist()

class GuildLister(object):
    __slots__=('guilds',)
    def __init__(self,client):
        guilds=[]
        sub_guilds=[]
        for guild in client.guild_profiles:
            sub_guilds.append(guild)
            
            if len(sub_guilds)==20:
                guilds.append(sub_guilds)
                sub_guilds=[]
                
        if sub_guilds:
            guilds.append(sub_guilds)
        del sub_guilds
        
        self.guilds=guilds

    def __len__(self):
        return self.guilds.__len__()

    def __getitem__(self, index):
        return Embed(description='\n'.join(f'- {guild.name}' for guild in self.guilds[index]))

        
@commands(case='server-list')
async def server_list(client, message, content):
    await Pagination(client, message.channel, GuildLister(client))

async def guild_create(client, guild):
    print(1)
    await client.message_create(CENTRAL_CHANNEL, f'- `{guild.name}` has added the bot!')

async def guild_delete(client, guild, profile):
    await client.message_create(CENTRAL_CHANNEL, f'- `{guild.name}` has removed the bot...')

def entry(client):
    client.events(guild_create)
    client.events(guild_delete)

def exit(client):
    del client.events.guild_create
    del client.events.guild_delete



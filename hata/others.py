# -*- coding: utf-8 -*-
__all__ = ('Relationship', 'AuditLogEvent', 'ContentFilterLevel',
    'DISCORD_EPOCH', 'FriendRequestFlag', 'Gift', 'GuildFeature',
    'HypesquadHouse', 'InviteTargetType', 'MFA', 'MessageActivity',
    'MessageFlag', 'MessageNotificationLevel', 'MessageType', 'PremiumType',
    'RelationshipType', 'Status', 'SystemChannelFlag', 'Theme', 'Unknown',
    'UserFlag', 'VerificationLevel', 'VoiceRegion', 'elapsed_time',
    'filter_content', 'id_to_time', 'is_id', 'is_mention', 'is_role_mention',
    'is_user_mention', 'now_as_id', 'parse_oauth2_redirect_url', 'random_id',
    'time_to_id', )

import random, re
from urllib.parse import _ALWAYS_SAFE_BYTES as ALWAYS_SAFE_BYTES,Quoter
from datetime import datetime
from base64 import b64encode
from time import time as time_now
from json import dumps as dump_to_json, loads as from_json
from dateutil.relativedelta import relativedelta

from .dereaddons_local import titledstr, modulize

#preparing encoding
safe='/ '.encode('ascii','ignore')
ALWAYS_SAFE_BYTES+=safe
QUOTER=Quoter(safe)
del safe,Quoter
def quote(text):
    #text must be str
    text=text.encode('utf-8','strict')
    if not text.rstrip(ALWAYS_SAFE_BYTES):
        return text.decode()
    return ''.join([QUOTER[char] for char in text])

#base64 conversions

def bytes_to_base64(data,ext=None):
    if ext is None:
        if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
            ext='image/png'
        elif data.startswith(b'\xFF\xD8') and data.rstrip(b'\0').endswith(b'\xFF\xD9'):
            ext='image/jpeg'
        elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
            ext='image/gif'
        else:
            raise ValueError('Unsupported image type given')
    return ''.join(['data:',ext,';base64,',b64encode(data).decode('ascii')])

def ext_from_base64(data):
    return data[11:data.find(';',11)]
    
DISCORD_EPOCH=1420070400000
#example date: "2016-03-31T19:15:39.954000+00:00"; "2019-04-28T15:14:38+00:00"
##parse_time=dateutil.parser.parse #can cause errors, commented till future reviews
##del dateutil

#old version:

#the RP32 would end on : "(\d{6}).*", but at message_update these dates can be
#rounded downwards, just to 3 decimal from the orginal 6
#Example:
#at edit        : "2019-07-17T18:52:50.758993+00:00" #this is before desuppress!
#at desuppress  : "2019-07-17T18:52:50.758000+00:00"

PARSE_TIME_RP32=re.compile('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{3}).*')
PARSE_TIME_RP25=re.compile('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.*')

def parse_time(timestamp):
    if len(timestamp)==32:
        pattern=PARSE_TIME_RP32
    elif len(timestamp)==25:
        pattern=PARSE_TIME_RP25
    else:
        raise ValueError(f'{timestamp!r} is not uses any of the defined patterns')
    return datetime(*map(int,pattern.match(timestamp).groups()))
    
#older version:
#def parse_time(timestamp):
#    return datetime(*map(int,re.split(r'[^\d]',timestamp.replace('+00:00',''))))

def id_to_time(id_):
    return datetime.utcfromtimestamp(((id_>>22)+DISCORD_EPOCH)/1000.)
        
def time_to_id(time):
    return ((time.timestamp()*1000.).__int__()-DISCORD_EPOCH)<<22

def random_id():
    return (((time_now()*1000.).__int__()-DISCORD_EPOCH)<<22)+(random.random()*4194304.).__int__()

def to_json(data):
    return dump_to_json(data,separators=(',',':'),ensure_ascii=True)

class VerificationLevel(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name
        
        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none    = NotImplemented
    low     = NotImplemented
    medium  = NotImplemented
    high    = NotImplemented
    extreme = NotImplemented

VerificationLevel.none     = VerificationLevel(0,'none')
VerificationLevel.low      = VerificationLevel(1,'low')
VerificationLevel.medium   = VerificationLevel(2,'medium')
VerificationLevel.high     = VerificationLevel(3,'high')
VerificationLevel.extreme  = VerificationLevel(4,'extreme')

class VoiceRegion(object):
    class _vr_dict(dict):
        def __missing__(self,id_):
            return VoiceRegion._from_id(id_)
    
    __slots__=('custom', 'deprecated', 'id', 'name', 'vip')
    values=_vr_dict()
    
    def __init__(self,name,id_,deprecated,vip):
        self.name       = name
        self.id         = id_
        self.deprecated = deprecated
        self.vip        = vip
        self.custom     = False
        self.values[id_]= self

    @classmethod
    def _from_id(cls,id_):
        name_parts      = id_.split('-')
        for index in range(len(name_parts)):
            name_part=name_parts[index]
            if len(name_part)<4:
                name_part=name_part.upper()
            else:
                name_part=name_part.capitalize()
            name_parts[index]=name_part
        
        name=' '.join(name_parts)
        
        self            = object.__new__(cls)
        self.name       = name
        self.id         = id_
        self.deprecated = False
        self.vip        = id_.startswith('vip-')
        self.custom     = True
        self.values[id_]= self
        return self
        
    @classmethod
    def from_data(cls,data):
        id_=data['id']
        if id_ in cls.values:
            return cls.values[id_]
        self            = object.__new__(cls)
        self.name       = data['name']
        self.id         = id_
        self.deprecated = data['deprecated']
        self.vip        = data['vip']
        self.custom     = data['custom']
        self.values[id_]= self
        return self
    
    def __str__(self):
        return self.id
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name!r} id={self.id!r}>'

    #normal
    brazil          = NotImplemented
    eu_central      = NotImplemented
    eu_west         = NotImplemented
    europe          = NotImplemented
    hongkong        = NotImplemented
    india           = NotImplemented
    japan           = NotImplemented
    russia          = NotImplemented
    singapore       = NotImplemented
    southafrica     = NotImplemented
    sydney          = NotImplemented
    us_central      = NotImplemented
    us_east         = NotImplemented
    us_south        = NotImplemented
    us_west         = NotImplemented
    #deprecated
    amsterdam       = NotImplemented
    frankfurt       = NotImplemented
    london          = NotImplemented
    #vip
    vip_us_east     = NotImplemented
    vip_us_west     = NotImplemented
    #vip + deprecated
    vip_amsterdam   = NotImplemented

VoiceRegion.brazil          = VoiceRegion('Brazil',         'brazil',       False,  False)
VoiceRegion.eu_central      = VoiceRegion('Central Europe', 'eu-central',   False,  False)
VoiceRegion.eu_west         = VoiceRegion('Western Europe', 'eu-west',      False,  False)
VoiceRegion.europe          = VoiceRegion('Europe',         'europe',       False,  False)
VoiceRegion.hongkong        = VoiceRegion('Hong Kong',      'hongkong',     False,  False)
VoiceRegion.india           = VoiceRegion('India',          'india',        False,  False)
VoiceRegion.japan           = VoiceRegion('Japan',          'japan',        False,  False)
VoiceRegion.russia          = VoiceRegion('Russia',         'russia',       False,  False)
VoiceRegion.singapore       = VoiceRegion('Singapore',      'singapore',    False,  False)
VoiceRegion.southafrica     = VoiceRegion('South Africa',   'southafrica',  False,  False)
VoiceRegion.sydney          = VoiceRegion('Sydney',         'sydney',       False,  False)
VoiceRegion.us_central      = VoiceRegion('US Central',     'us-central',   False,  False)
VoiceRegion.us_east         = VoiceRegion('US East',        'us-east',      False,  False)
VoiceRegion.us_south        = VoiceRegion('US South',       'us-south',     False,  False)
VoiceRegion.us_west         = VoiceRegion('US West',        'us-west',      False,  False)
#deprecated
VoiceRegion.amsterdam       = VoiceRegion('Amsterdam',      'amsterdam',    True,   False)
VoiceRegion.frankfurt       = VoiceRegion('Frankfurt',      'frankfurt',    True,   False)
VoiceRegion.london          = VoiceRegion('London',         'london',       True,   False)
#vip
VoiceRegion.vip_us_east     = VoiceRegion('VIP US West',    'vip-us-west',  False,  True)
VoiceRegion.vip_us_west     = VoiceRegion('VIP US East',    'vip-us-east',  False,  True)
#vip + deprecated
VoiceRegion.vip_amsterdam   = VoiceRegion('VIP Amsterdam',  'vip-amsterdam',True,   True)

class ContentFilterLevel(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    disabled    = NotImplemented
    no_role     = NotImplemented
    everyone    = NotImplemented

ContentFilterLevel.disabled = ContentFilterLevel(0,'disabled')
ContentFilterLevel.no_role  = ContentFilterLevel(1,'no_role')
ContentFilterLevel.everyone = ContentFilterLevel(2,'everyone')

class HypesquadHouse(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    bravery     = NotImplemented
    brilliance  = NotImplemented
    balance     = NotImplemented

HypesquadHouse.bravery      = HypesquadHouse(1,'bravery')
HypesquadHouse.brilliance   = HypesquadHouse(2,'brilliance')
HypesquadHouse.balance      = HypesquadHouse(3,'balance')


class Status(object):
    __slots__=('position', 'value')
    values={}
    def __init__(self,value,position):
        self.value=value
        self.position=position
        self.values[value]=self

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'<{self.__class__.__name__} value={self.value!r}>'

    def __gt__(self,other):
        if type(self) is type(other):
            return self.position>other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position>other.position
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.position>=other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position>=other.position
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.position==other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position==other.position
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.position!=other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position!=other.position
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.position<=other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position<=other.position
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.position<other.position
        if isinstance(other,str):
            try:
                other=type(self).values[other]
            except KeyError:
                return NotImplemented
            return self.position<other.position
        return  NotImplemented

    name=property(__str__)

    online      = NotImplemented
    idle        = NotImplemented
    dnd         = NotImplemented
    offline     = NotImplemented
    invisible   = NotImplemented

Status.online   = Status('online',0)
Status.idle     = Status('idle',1)
Status.dnd      = Status('dnd',2)
Status.offline  = Status('offline',3)
Status.invisible= Status('invisible',3)

class MessageNotificationLevel(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    all_messages    = NotImplemented
    only_mentions   = NotImplemented
    
MessageNotificationLevel.all_messages   = MessageNotificationLevel(0,'all_messages')
MessageNotificationLevel.only_mentions  = MessageNotificationLevel(1,'only_mentions')

class MFA(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none    = NotImplemented
    elevated= NotImplemented

MFA.none    = MFA(0,'none')
MFA.elevated= MFA(1,'elevated')

class PremiumType(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none            = NotImplemented
    nitro_classic   = NotImplemented
    nitro           = NotImplemented

PremiumType.none            = PremiumType(0,'none')
PremiumType.nitro_classic   = PremiumType(1,'nitro_classic')
PremiumType.nitro           = PremiumType(2,'nitro')

class UserFlag(int):
    __slots__=()
    
    @property
    def discord_employee(self):
        return self&1
    
    @property
    def discord_partner(self):
        return (self>>1)&1
    
    @property
    def hypesquad_events(self):
        return (self>>2)&1
    
    @property
    def bug_hunter(self):
        return (self>>3)&1
    
    @property
    def hypesquad_bravery(self):
        return (self>>6)&1
    
    @property
    def hypesquad_brilliance(self):
        return (self>>7)&1
    
    @property
    def hypesquad_balance(self):
        return (self>>8)&1
    
    @property
    def early_supporter(self):
        return (self>>9)&1

    @property
    def team_user(self):
        return (self>>10)&1
    
    def __iter__(self):
        if self&1:
            yield 'discord_employee'
        if (self>>1)&1:
            yield 'discord_partner'
        if (self>>2)&1:
            yield 'bug_hunter'
        if (self>>3)&1:
            yield 'hypesquad_bravery'
        if (self>>6)&1:
            yield 'hypesquad_bravery'
        if (self>>7)&1:
            yield 'hypesquad_brilliance'
        if (self>>8)&1:
            yield 'hypesquad_balance'
        if (self>>9)&1:
            yield 'early_supporter'
        if (self>>10)&1:
            yield 'team_user'

    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

class MessageFlag(int):
    __slots__=()

    @property
    def crossposted(self):
        return self&1

    @property
    def is_crosspost(self):
        return (self>>1)&1

    @property
    def embeds_suppressed(self):
        return (self>>2)&1

    def __iter__(self):
        if self&1:
            yield 'crossposted'
        if (self>>1)&1:
            yield 'is_crosspost'
        if (self>>2)&1:
            yield 'embeds_suppressed'

    def __repr__(self):
        return f'{self.__class__.__name__}({int.__repr__(self)})'

class RelationshipType(object):
    __slots__=('name', 'value',)
    values=[None,None,None,None,None]
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    stranger        = NotImplemented
    friend          = NotImplemented
    blocked         = NotImplemented
    received_request= NotImplemented
    sent_request    = NotImplemented

RelationshipType.stranger         = RelationshipType(0,'stranger')
RelationshipType.friend           = RelationshipType(1,'friend')
RelationshipType.blocked          = RelationshipType(2,'blocked')
RelationshipType.received_request = RelationshipType(3,'received_request')
RelationshipType.sent_request     = RelationshipType(4,'sent_request')

class Relationship(object):
    __slots__=('type', 'user')
    def __init__(self,client,user,data):
        self.user=user
        self.type=RelationshipType.values[data['type']]
        client.relationships[user.id]=self
        
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.type.name} user={self.user.full_name}>'


class MessageType(object):
    __slots__=('name', 'value', 'convert')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name
        self.convert=self._default_convert

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    @staticmethod
    def _default_convert(self):
        pass

    default                 = NotImplemented
    add_user                = NotImplemented
    remove_user             = NotImplemented
    call                    = NotImplemented
    channel_name_change     = NotImplemented
    channel_icon_change     = NotImplemented
    new_pin                 = NotImplemented
    new_member              = NotImplemented
    new_guild_sub           = NotImplemented
    new_guild_sub_t1        = NotImplemented
    new_guild_sub_t2        = NotImplemented
    new_guild_sub_t3        = NotImplemented
    new_follower_channel    = NotImplemented

MessageType.default               = MessageType(0,'default')
MessageType.add_user              = MessageType(1,'add_user')
MessageType.remove_user           = MessageType(2,'remove_user')
MessageType.call                  = MessageType(3,'call')
MessageType.channel_name_change   = MessageType(4,'channel_name_change')
MessageType.channel_icon_change   = MessageType(5,'channel_icon_change')
MessageType.new_pin               = MessageType(6,'new_pin')
MessageType.new_member            = MessageType(7,'new_member')
MessageType.new_guild_sub         = MessageType(8,'new_guild_sub')
MessageType.new_guild_sub_t1      = MessageType(9,'new_guild_sub_t1')
MessageType.new_guild_sub_t2      = MessageType(10,'new_guild_sub_t2')
MessageType.new_guild_sub_t3      = MessageType(11,'new_guild_sub_t3')
MessageType.new_follower_channel  = MessageType(12,'new_follower_channel')

class MessageActivity(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    none        = NotImplemented
    join        = NotImplemented
    spectate    = NotImplemented
    listen      = NotImplemented
    join_request= NotImplemented

MessageActivity.none           = MessageActivity(0,'none')
MessageActivity.join           = MessageActivity(1,'join')
MessageActivity.spectate       = MessageActivity(2,'spectate')
MessageActivity.listen         = MessageActivity(3,'listen')
MessageActivity.join_request   = MessageActivity(5,'join_request')

class AuditLogEvent(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    GUILD_UPDATE            = NotImplemented
    
    CHANNEL_CREATE          = NotImplemented
    CHANNEL_UPDATE          = NotImplemented
    CHANNEL_DELETE          = NotImplemented
    CHANNEL_OVERWRITE_CREATE= NotImplemented
    CHANNEL_OVERWRITE_UPDATE= NotImplemented
    CHANNEL_OVERWRITE_DELETE= NotImplemented
    
    MEMBER_KICK             = NotImplemented
    MEMBER_PRUNE            = NotImplemented
    MEMBER_BAN_ADD          = NotImplemented
    MEMBER_BAN_REMOVE       = NotImplemented
    MEMBER_UPDATE           = NotImplemented
    MEMBER_ROLE_UPDATE      = NotImplemented
    MEMBER_MOVE             = NotImplemented
    MEMBER_DISCONNECT       = NotImplemented
    BOT_ADD                 = NotImplemented
    
    ROLE_CREATE             = NotImplemented
    ROLE_UPDATE             = NotImplemented
    ROLE_DELETE             = NotImplemented
    
    INVITE_CREATE           = NotImplemented
    INVITE_UPDATE           = NotImplemented
    INVITE_DELETE           = NotImplemented
    
    WEBHOOK_CREATE          = NotImplemented
    WEBHOOK_UPDATE          = NotImplemented
    WEBHOOK_DELETE          = NotImplemented
    
    EMOJI_CREATE            = NotImplemented
    EMOJI_UPDATE            = NotImplemented
    EMOJI_DELETE            = NotImplemented
    
    MESSAGE_DELETE          = NotImplemented
    MESSAGE_BULK_DELETE     = NotImplemented
    MESSAGE_PIN             = NotImplemented
    MESSAGE_UNPIN           = NotImplemented
    
    INTEGRATION_CREATE      = NotImplemented
    INTEGRATION_UPDATE      = NotImplemented
    INTEGRATION_DELETE      = NotImplemented

AuditLogEvent.GUILD_UPDATE              = AuditLogEvent( 1,'GUILD_UPDATE')

AuditLogEvent.CHANNEL_CREATE            = AuditLogEvent(10,'CHANNEL_CREATE')
AuditLogEvent.CHANNEL_UPDATE            = AuditLogEvent(11,'CHANNEL_UPDATE')
AuditLogEvent.CHANNEL_DELETE            = AuditLogEvent(12,'CHANNEL_DELETE')
AuditLogEvent.CHANNEL_OVERWRITE_CREATE  = AuditLogEvent(13,'CHANNEL_OVERWRITE_CREATE')
AuditLogEvent.CHANNEL_OVERWRITE_UPDATE  = AuditLogEvent(14,'CHANNEL_OVERWRITE_UPDATE')
AuditLogEvent.CHANNEL_OVERWRITE_DELETE  = AuditLogEvent(15,'CHANNEL_OVERWRITE_DELETE')

AuditLogEvent.MEMBER_KICK               = AuditLogEvent(20,'MEMBER_KICK')
AuditLogEvent.MEMBER_PRUNE              = AuditLogEvent(21,'MEMBER_PRUNE')
AuditLogEvent.MEMBER_BAN_ADD            = AuditLogEvent(22,'MEMBER_BAN_ADD')
AuditLogEvent.MEMBER_BAN_REMOVE         = AuditLogEvent(23,'MEMBER_BAN_REMOVE')
AuditLogEvent.MEMBER_UPDATE             = AuditLogEvent(24,'MEMBER_UPDATE')
AuditLogEvent.MEMBER_ROLE_UPDATE        = AuditLogEvent(25,'MEMBER_ROLE_UPDATE')
AuditLogEvent.MEMBER_MOVE               = AuditLogEvent(26,'MEMBER_MOVE')
AuditLogEvent.MEMBER_DISCONNECT         = AuditLogEvent(27,'MEMBER_DISCONNECT')
AuditLogEvent.BOT_ADD                   = AuditLogEvent(28,'MEMBER_ROLE_UPDATE')

AuditLogEvent.ROLE_CREATE               = AuditLogEvent(30,'ROLE_CREATE')
AuditLogEvent.ROLE_UPDATE               = AuditLogEvent(31,'ROLE_UPDATE')
AuditLogEvent.ROLE_DELETE               = AuditLogEvent(32,'ROLE_DELETE')

AuditLogEvent.INVITE_CREATE             = AuditLogEvent(40,'INVITE_CREATE')
AuditLogEvent.INVITE_UPDATE             = AuditLogEvent(41,'INVITE_UPDATE')
AuditLogEvent.INVITE_DELETE             = AuditLogEvent(42,'INVITE_DELETE')

AuditLogEvent.WEBHOOK_CREATE            = AuditLogEvent(50,'WEBHOOK_CREATE')
AuditLogEvent.WEBHOOK_UPDATE            = AuditLogEvent(51,'WEBHOOK_UPDATE')
AuditLogEvent.WEBHOOK_DELETE            = AuditLogEvent(52,'WEBHOOK_DELETE')

AuditLogEvent.EMOJI_CREATE              = AuditLogEvent(60,'EMOJI_CREATE')
AuditLogEvent.EMOJI_UPDATE              = AuditLogEvent(61,'EMOJI_UPDATE')
AuditLogEvent.EMOJI_DELETE              = AuditLogEvent(62,'EMOJI_DELETE')

AuditLogEvent.MESSAGE_DELETE            = AuditLogEvent(72,'MESSAGE_DELETE')
AuditLogEvent.MESSAGE_BULK_DELETE       = AuditLogEvent(73,'MESSAGE_BULK_DELETE')
AuditLogEvent.MESSAGE_PIN               = AuditLogEvent(74,'MESSAGE_PIN')
AuditLogEvent.MESSAGE_UNPIN             = AuditLogEvent(75,'MESSAGE_UNPIN')

AuditLogEvent.INTEGRATION_CREATE        = AuditLogEvent(80,'INTEGRATION_CREATE')
AuditLogEvent.INTEGRATION_UPDATE        = AuditLogEvent(81,'INTEGRATION_UPDATE')
AuditLogEvent.INTEGRATION_DELETE        = AuditLogEvent(82 ,'INTEGRATION_DELETE')


def multi_delete_time_limit():
    #2 weeks-1 minute since now, so if we delete a lot of messages, it wont mess up
    return int((time_now()-1209540.)*1000.-DISCORD_EPOCH)<<22

def log_time_converter(value):
    if hasattr(value,'id'):
        return value.id
    if isinstance(value,int):
        return value
    if isinstance(value,datetime):
        return time_to_id(value)

    raise TypeError

IS_ID_RP=re.compile('(\d{7,21})')
IS_MENTION_RP=re.compile('@everyone|@here|<@[!&]?\d{7,21}>|<#\d{7,21}>')

USER_MENTION_RP=re.compile('<@!?(\d{7,21})>')
CHANNEL_MENTION_RP=re.compile('<#(\d{7,21})>')
ROLE_MENTION_RP=re.compile('<@&(\d{7,21})>')

EMOJI_RP=re.compile('<([a]{0,1}):([a-zA-Z0-9_]{2,32}(~[1-9]){0,1}):(\d{7,21})>')
EMOJI_NAME_RP=re.compile(':{0,1}([a-zA-Z0-9_\\-~]{1,32}):{0,1}')
FILTER_RP=re.compile('("(.+?)"|\S+)')
OA2_RU_RP=re.compile('(https{0,1}://.+?)\?code=([a-zA-Z0-9]{30})')

def is_id(text):
    return IS_ID_RP.fullmatch(text) is not None

def is_mention(text):
    return IS_MENTION_RP.fullmatch(text) is not None

def is_user_mention(text):
    return USER_MENTION_RP.fullmatch(text) is not None

def is_channel_mention(text):
    return CHANNEL_MENTION_RP.fullmatch(text) is not None

def is_role_mention(text):
    return ROLE_MENTION_RP.fullmatch(text) is not None

def now_as_id():
    return ((time_now()*1000.)-DISCORD_EPOCH).__int__()<<22

#thanks Pythonic#6090 for the simple design
def filter_content(content):
    return [match[1] or match[0] for match in FILTER_RP.findall(content)]

def parse_oauth2_redirect_url(url):
    result=OA2_RU_RP.fullmatch(url)
    if result is None:
        raise ValueError
    return result.groups()


def chunkify(lines,limit=2000):
    result=[]
    ln_count=0
    shard=[]
    for line in lines:
        ln=len(line)+1
        ln_count+=ln
        if ln_count>limit:
            ln_count=ln
            result.append('\n'.join(shard))
            shard.clear()
        shard.append(line)
    result.append('\n'.join(shard))
    return result

def cchunkify(lines,lang='',limit=2000):
    limit=limit-4
    starter=f'```{lang}'
    ln_starter=len(starter)
    
    result=[]
    ln_count=ln_starter
    shard=[starter]
    for line in lines:
        ln=len(line)+1
        ln_count+=ln
        if ln_count>limit:
            ln_count=ln+ln_starter
            shard.append('```')
            result.append('\n'.join(shard))
            shard.clear()
            shard.append(starter)
        shard.append(line)
    if len(shard)>1:
        shard.append('```')
        result.append('\n'.join(shard))
    return result

def elapsed_time(obj,limit=3,names=('years','months','days','hours','minutes','seconds')):
    if type(obj) is datetime:
        delta=relativedelta(datetime.utcnow(),obj)
    elif type(obj) is relativedelta:
        delta=obj
    else:
        raise TypeError(f'Expected, relativedelta or datetime, got {obj!r}')
        
    values=(delta.years,delta.months,delta.days,delta.hours,delta.minutes,delta.seconds)
    result=[]
    is_higher=None
    for index in range(6):
        value=values[index]
        if is_higher is not None:
            result.append(value)
            continue
        if value:
            is_higher=index
            result.append(value)

    del result[limit:]

    text=[]
    for value,name in zip(result,names[is_higher:]):
        if value<0:
            value=-value
        text.append(f'{value} {name}')
    return ', '.join(text)

class GuildFeature(object):
    class _gf_dict(dict):
        def __missing__(self,name):
            return GuildFeature(name)
    
    values=_gf_dict()
    
    __slots__=('value',)

    def __init__(self,value):
        self.value=value
        self.values[value]=self
    
    def __str__(self):
        return self.value

    name=property(__str__)
    
    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def __gt__(self,other):
        if type(self) is type(other):
            return self.value>other.value
        if isinstance(other,str):
            return self.value>other
        return NotImplemented

    def __ge__(self,other):
        if type(self) is type(other):
            return self.value>=other.value
        if isinstance(other,str):
            return self.value>=other
        return NotImplemented

    def __eq__(self,other):
        if type(self) is type(other):
            return self.value==other.value
        if isinstance(other,str):
            return self.value==other
        return NotImplemented

    def __ne__(self,other):
        if type(self) is type(other):
            return self.value!=other.value
        if isinstance(other,str):
            return self.value!=other
        return NotImplemented

    def __le__(self,other):
        if type(self) is type(other):
            return self.value<=other.value
        if isinstance(other,str):
            return self.value<=other
        return NotImplemented

    def __lt__(self,other):
        if type(self) is type(other):
            return self.value<other.value
        if isinstance(other,str):
            return self.value<other
        return  NotImplemented

    splash              = NotImplemented
    vip                 = NotImplemented
    vanity              = NotImplemented
    animated_icon       = NotImplemented
    verified            = NotImplemented
    partnered           = NotImplemented
    more_emoji          = NotImplemented
    discoverable        = NotImplemented
    commerce            = NotImplemented
    public              = NotImplemented
    news                = NotImplemented
    banner              = NotImplemented
    member_list_disabled= NotImplemented

GuildFeature.splash                 = GuildFeature('INVITE_SPLASH')
GuildFeature.vip                    = GuildFeature('VIP_REGIONS')
GuildFeature.vanity                 = GuildFeature('VANITY_URL')
GuildFeature.animated_icon          = GuildFeature('ANIMATED_ICON')
GuildFeature.verified               = GuildFeature('VERIFIED')
GuildFeature.partnered              = GuildFeature('PARTNERED')
GuildFeature.more_emoji             = GuildFeature('MORE_EMOJI')
GuildFeature.discoverable           = GuildFeature('DISCOVERABLE')
GuildFeature.commerce               = GuildFeature('COMMERCE')
GuildFeature.public                 = GuildFeature('PUBLIC')
GuildFeature.news                   = GuildFeature('NEWS')
GuildFeature.banner                 = GuildFeature('BANNER')
GuildFeature.member_list_disabled   = GuildFeature('MEMBER_LIST_DISABLED')

class Unknown(object):
    __slots__=('id', 'name', 'type')
    def __init__(self,type_,id_,name=''):
        self.type=type_
        self.id=id_
        if name:
            self.name=name
        else:
            self.name=type_
    
    def __repr__(self):
        return f'<{self.__class__.__name__} type={self.type} id={self.id} name=\'{self.name}\'>'

    def __gt__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id>other_id
        
        return NotImplemented
        
    def __ge__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id>=other_id
        
        return NotImplemented
    
    def __eq__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id==other_id
        
        return NotImplemented
    
    def __ne__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id!=other_id
        
        return NotImplemented
    
    def __le__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id<=other_id
        
        return NotImplemented
    
    def __lt__(self,other):
        try:
            other_id=other.id
        except AttributeError:
            return NotImplemented
        
        if self.name in other.__class__.__name__:
            return self.id<other_id
        
        return NotImplemented

    @property
    def created_at(self):
        return id_to_time(self.id)
    
class InviteTargetType(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'

    NONE    = NotImplemented
    STREAM  = NotImplemented

InviteTargetType.NONE   = InviteTargetType(0,'NONE')
InviteTargetType.STREAM = InviteTargetType(1,'STREAM')


#parse image hash formats
def _parse_ih_fs(value):
    if value is None:
        return 0
    if type(value) is str:
        return int(value,16)
    if type(value) is int:
        return value
    raise TypeError(f'Image hash can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}')

#parse image hash formats animated
def _parse_ih_fsa(value,animated):
    if type(animated) is not bool:
        raise TypeError('Animated should be type bool, got {animated.__class__.__name__}')
    if value is None:
        return 0,False
    if type(value) is str:
        if value.startswith('a_'):
            return int(value[2:],16),True
        return int(value,16),animated
    if type(value) is int:
        return value,animated
    raise TypeError(f'Image hash can be `NoneType`, `str` or `int` type, got {value.__class__.__name__}')

class FriendRequestFlag(object):
    __slots__=('name', 'value')
    values={}
    def __init__(self,value,name):
        self.value=value
        self.name=name

        self.values[value]=self

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, name=\'{self.name}\')'
    
    @classmethod
    def decode(cls,data):
        if data is None:
            return cls.none
        
        all_=data.get('all',False)
        if all_:
            key=4
        else:
            mutual_guilds=data.get('mutual_guilds',False)
            mutual_friends=data.get('mutual_friends',False)
            
            key=mutual_guilds+(mutual_friends<<1)
        
        return cls.values[key]
    
    def encode(self):
        value=self.value
        if value==0:
            return {}
        
        if value==1:
            return {'mutual_guilds': True}
        
        if value==2:
            return {'mutual_friends': True}
        
        if value==3:
            return {'mutual_guilds': True, 'mutual_friends': True}
        
        if value==4:
            return {'all': True}
        
        # should not happen
        return {}
    
    none                        = NotImplemented
    mutual_guilds               = NotImplemented
    mutual_friends              = NotImplemented
    mutual_guilds_and_friends   = NotImplemented
    all                         = NotImplemented

FriendRequestFlag.none                      = FriendRequestFlag(0,'none')
FriendRequestFlag.mutual_guilds             = FriendRequestFlag(1,'mutual_guilds')
FriendRequestFlag.mutual_friends            = FriendRequestFlag(2,'mutual_friends')
FriendRequestFlag.mutual_guilds_and_friends = FriendRequestFlag(3,'mutual_guilds_and_friends')
FriendRequestFlag.all                       = FriendRequestFlag(4,'all')

class Theme(object):
    __slots__=('value',)
    values={}
    def __init__(self,value):
        self.value=value
        self.values[value]=self

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'<{self.__class__.__name__} value={self.value!r}>'

    @property
    def name(self):
        return self.value

    dark    = NotImplemented
    light   = NotImplemented

Theme.dark  = Theme('dark')
Theme.light = Theme('light')

class SystemChannelFlag(int):
    __slots__=[]
    
    @property
    def none(self):
        return self==0b11

    @property
    def all(self):
        return self==0b00
    
    @property
    def welcome(self):
        return (self&1)^1
    
    @property
    def boost(self):
        return ((self>>1)&1)^1
    
    def __iter__(self):
        if not self&1:
            yield 'welcome'
        if not (self>>1)&1:
            yield 'boost'

    def __repr__(self):
        return f'{self.__class__.__name__}({self!s})'

    NONE    = NotImplemented
    ALL     = NotImplemented

SystemChannelFlag.NONE  = SystemChannelFlag(0b11)
SystemChannelFlag.ALL   = SystemChannelFlag(0b00)

class Gift(object):
    __slots__=('uses', 'code')
    def __init__(self,data):
        self.uses=data['uses']
        self.code=data['code']

@modulize
class Discord_hdrs:
    #to receive
    AUDIT_LOG_REASON=titledstr('X-Audit-Log-Reason')
    RATELIMIT_REMAINING=titledstr('X-Ratelimit-Remaining')
    RATELIMIT_RESET=titledstr('X-Ratelimit-Reset')
    RATELIMIT_RESET_AFTER=titledstr('X-Ratelimit-Reset-After')

    #to send
    RATELIMIT_PRECISION=titledstr.by_pass_titling('X-RateLimit-Precision')

del re, titledstr, modulize


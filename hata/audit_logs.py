# -*- coding: utf-8 -*-
__all__ = ('AuditLog', 'AuditLogEntry', 'AuditLogIterator', )

from .others import AuditLogEvent, VerificationLevel, ContentFilterLevel,   \
    Unknown, now_as_id,id_to_time
from .client_core import INTEGRATIONS, CHANNELS, USERS, ROLES, EMOJIS
from .permission import Permission
from .color import Color
from .user import User
from .webhook import Webhook
from .role import PermOW

class AuditLog(object):
    __slots__=('guild', 'logs', 'users', 'webhooks',)
    def __init__(self,data,guild):
        self.guild=guild
        
        self.webhooks=webhooks={}
        try:
            webhook_datas=data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhook_datas:
                webhook=Webhook(webhook_data)
                webhooks[webhook.id]=webhook

        self.users=users={}
        try:
            user_datas=data['users']
        except KeyError:
            pass
        else:
            for user_data in user_datas:
                user=User(user_data)
                users[user.id]=user
        
        try:
            log_datas=data['audit_log_entries']
        except KeyError:
            self.logs=[]
        else:
            self.logs=[AuditLogEntry(log_data,guild,webhooks,users) for log_data in log_datas]
    
    def __iter__(self):
        return self.logs.__iter__()

    def __len__(self):
        return self.logs.__len__()


class AuditLogIterator(object):
    __slots__=('data', 'guild', 'client', 'index', 'logs', 'users', 'webhooks',)
    def __init__(self,client,guild,user=None,event=None):
        self.guild=guild
        self.index=0

        self.data = {
            'limit' : 100,
            'before': now_as_id(),
                }

        if user is not None:
            self.data['user_id']=user.id
        if event is not None:
            self.data['action_type']=event.value
        
        self.client=client
        self.webhooks={}
        self.users={}
        self.logs=[]

    async def load_all(self):
        logs=self.logs
        client=self.client
        http=client.http
        while True:
            if logs:
                self.data['before']=logs[-1].id
            data = await http.audit_logs(self.guild.id,self.data)
            try:
                self._process_data(data)
            except StopAsyncIteration:
                return
            if len(logs)%100:
                return
            
    def transform(self):
        result=object.__new__(AuditLog)
        result.guild=self.guild
        result.webhooks=self.webhooks
        result.users=self.users
        result.logs=self.logs
        return result
    
    def __aiter__(self):
        return self

    async def __anext__(self):
        ln=len(self.logs)
        index=self.index
        if index<ln:
            self.index+=1
            return self.logs[index]
        if index%100:
            raise StopAsyncIteration
        if ln:
            self.data['before']=self.logs[ln-1].id
        data = await self.client.http.audit_logs(self.guild.id,self.data)
        self._process_data(data)
        self.index+=1
        return self.logs[index]
        
    def _process_data(self,data):
        try:
            log_datas=data['audit_log_entries']
            if not log_datas:
                raise StopAsyncIteration
        except KeyError:
            raise StopAsyncIteration from None

        webhooks=self.webhooks
        try:
            webhooks_data=data['webhook']
        except KeyError:
            pass
        else:
            for webhook_data in webhooks_data:
                webhook=Webhook(webhook_data)
                webhooks[webhook.id]=webhook

        users=self.users
        try:
            users_data=data['users']
        except KeyError:
            pass
        else:
            for user_data in users_data:
                user=User(user_data)
                self.users[user.id]=user

        logs=self.logs
        guild=self.guild
        for log_data in log_datas:
            logs.append(AuditLogEntry(log_data,guild,webhooks,users))
        
def convert_guild(self,guild,webhooks,users,target_id):
    return guild

def convert_channel(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.all_channel[id_]
    except KeyError:
        #what can we do?
        return Unknown('Channel',id_)

def convert_user(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return USERS[id_]
    except KeyError:
        return Unknown('User',id_)

def convert_role(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.all_role[id_]
    except KeyError:
        return Unknown('Role',id_)

def convert_invite(self,guild,webhooks,users,target_id):
    #every other data is at #change
    for change in self.changes:
        if change.attr!='code':
            continue
        
        if self.type is AuditLogEvent.INVITE_DELETE:
            code=change.before
        else:
            code=change.after
        break
    
    else:
        code='' #malformed ?
    
    return Unknown('Invite',code)

def convert_webhook(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return webhooks[id_]
    except KeyError:
        return Unknown('Webhook',id_)

def convert_emoji(self,guild,webhooks,users,target_id):
    id_=int(target_id)
    try:
        return guild.emojis[id_]
    except KeyError:
        try:
            return EMOJIS[id_]
        except KeyError:
            return Unknown('Emoji',id_)

def convert_message(self,guild,webhooks,users,target_id):
    # TODO: test for bulk, is target_id a list?
    # we wont waste time on message search
    return Unknown('Message',int(target_id))

def convert_integration(self,guild,webhooks,users,target_id):
    # TODO: test, I have no integration to test this endpoint
    id_=int(target_id)
    try:
        return INTEGRATIONS[id_]
    except KeyError:
        return Unknown('Integration',id_)

CONVERSIONS = (
    convert_guild,
    convert_channel,
    convert_user,
    convert_role,
    convert_invite,
    convert_webhook,
    convert_emoji,
    convert_message,
    convert_integration,
        )

del convert_guild
del convert_channel
del convert_user
del convert_role
del convert_invite
del convert_webhook
del convert_emoji
del convert_message
del convert_integration

class AuditLogEntry(object):
    __slots__=('changes', 'id', 'options', 'reason', 'target', 'type', 'user',)
    def __init__(self,data,guild,webhooks,users):
        self.id=int(data['id'])
        self.type=AuditLogEvent.values[int(data['action_type'])]
        try:
            options=data['options']
        except KeyError:
            self.options=None
        else:
            self.options=options
            for key,value in options.items():
                if key.endswith('id'):
                    options[key]=int(value)
        user_id=data.get('user_id',None)
        if user_id is None:
            self.user=None
        else:
            self.user=users[int(user_id)]

        self.reason=data.get('reason',None)
        changes=data.get('changes',None)
        if changes is None:
            self.changes=None
        else:
            transformed_changes=[]
            self.changes=transformed_changes
            for element in changes:
                try:
                    key=element['key']
                except KeyError: #malformed?
                    continue
                try:
                    transformer=TRANSFORMERS[key]
                except KeyError:
                    transformer=transform_nothing
                
                transformed_changes.append(transformer(key,element))
        
        try:
            target_id=data['target_id']
        except KeyError:
            self.target=None
        else:
            self.target=CONVERSIONS[self.type.value//10](self,guild,webhooks,users,target_id)

    @property
    def created_at(self):
        return id_to_time(self.id)

def PermOW_from_logs(data):
    self=object.__new__(PermOW)
    id_=int(data['id'])
    if data['type']=='role':
        try:
            self.target=ROLES[id_]
        except KeyError:
            self.target=Unknown('Role',id_)
    else:
        try:
            self.target=USERS[id_]
        except KeyError:
            self.target=Unknown('User',id_)
    
    self.allow=data['allow']
    self.deny=data['deny']

    return self

def transform_nothing(name,data):
    change=AuditLogChange()
    change.attr=name
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_verification_level(name,data):
    change=AuditLogChange()
    change.attr='verification_level'
    value=data.get('old_value',None)
    change.before=None if value is None else VerificationLevel.value[value]
    value=data.get('new_value',None)
    change.after=None if value is None else VerificationLevel.value[value]
    return change

def transform_content_filter(name,data):
    change=AuditLogChange()
    change.attr='content_filter'
    value=data.get('old_value',None)
    change.before=None if value is None else ContentFilterLevel.values[value]
    value=data.get('new_value',None)
    change.after=None if value is None else ContentFilterLevel.values[value]
    return change

def transform_permissions(name,data):
    change=AuditLogChange()
    change.attr=name
    value=data.get('old_value',None)
    change.before=None if value is None else Permission(value)
    value=data.get('new_value',None)
    change.after=None if value is None else Permission(value)
    return change

def transform_snowfalke(name,data):
    change=AuditLogChange()
    change.attr=name
    value=data.get('old_value',None)
    change.before=None if value is None else int(value)
    value=data.get('new_value',None)
    change.after=None if value is None else int(value)
    return change

def transform_color(name,data):
    change=AuditLogChange()
    change.attr=name
    value=data.get('old_value',None)
    change.before=None if value is None else Color(value)
    value=data.get('new_value',None)
    change.after=None if value is None else Color(value)
    return change

def transform_user(name,data):
    change=AuditLogChange()
    change.attr=name[:-3]
    value=data.get('old_value',None)
    if value is None:
        change.before=None
    else:
        value=int(value)
        try:
            change.before=USERS[value]
        except KeyError:
            change.before=Unknown('User',value)
    value=data.get('new_value',None)
    if value is None:
        change.after=None
    else:
        value=int(value)
        try:
            change.after=USERS[value]
        except KeyError:
            change.after=Unknown('User',value)
    return change

def transform_channel(name,data):
    change=AuditLogChange()
    change.attr=name[:-3]
    value=data.get('old_value',None)
    if value is None:
        change.before=None
    else:
        value=int(value)
        try:
            change.before=CHANNELS[value]
        except KeyError:
            change.before=Unknown('Channel',value)
    value=data.get('new_value',None)
    if value is None:
        change.after=None
    else:
        value=int(value)
        try:
            change.after=CHANNELS[value]
        except KeyError:
            change.after=Unknown('Channel',value)
    return change

def transform_overwrites(name,data):
    change=AuditLogChange()
    change.attr='overwrites'
    value=data.get('old_value',None)
    change.before=None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    value=data.get('new_value',None)
    change.after=None if value is None else [PermOW_from_logs(ow_data) for ow_data in value]
    return change

def transform_int__slowmode(name,data):
    change=AuditLogChange()
    change.attr='slowmode'
    change.before=data.get('old_value',None)
    change.after=data.get('new_value',None)
    return change

def transform_avatar(name,data):
    change=AuditLogChange()
    change.attr=name[:-5]

    avatar=data.get('old_value',None)
    if avatar is None:
        avatar=0
        has_animated_avatar=False
    elif avatar.startswith('a_'):
        avatar=int(avatar[2:],16)
        has_animated_avatar=True
    else:
        avatar=int(avatar,16)
        has_animated_avatar=False
    
    change.before=(has_animated_avatar,avatar)
    
    avatar=data.get('new_value',None)
    if avatar is None:
        avatar=0
        has_animated_avatar=False
    elif avatar.startswith('a_'):
        avatar=int(avatar[2:],16)
        has_animated_avatar=True
    else:
        avatar=int(avatar,16)
        has_animated_avatar=False
    
    change.after=(has_animated_avatar,avatar)
    
    return change

def transform_role(name,data):
    change=AuditLogChange()
    change.attr='role'
    if name=='$add':
        change.before=None
        change.after=roles=[]
    else:
        change.before=roles=[]
        change.after=None

    for element in data['new_value']:
        role_id=int(element['id'])
        try:
            role=ROLES[role_id]
        except KeyError:
            role=Unknown('Role',role_id,element['name'])
        roles.append(role)

    return change

TRANSFORMERS = {
    'verification_level'    : transform_verification_level,
    'explicit_content_filter':transform_content_filter,
    'allow'                 : transform_permissions,
    'deny'                  : transform_permissions,
    'permissions'           : transform_permissions,
    'id'                    : transform_snowfalke,
    'account_id'            : transform_snowfalke,
    'color'                 : transform_color,
    'owner_id'              : transform_user,
    'inviter_id'            : transform_user,
    'channel_id'            : transform_channel,
    'afk_channel_id'        : transform_channel,
    'system_channel_id'     : transform_channel,
    'widget_channel_id'     : transform_channel,
    'permission_overwrites' : transform_overwrites,
    'rate_limit_per_user'   : transform_int__slowmode,
    'splash_hash'           : transform_avatar,
    'icon_hash'             : transform_avatar,
    'avatar_hash'           : transform_avatar,
    '$add'                  : transform_role,
    '$remove'               : transform_role,
        }

del transform_verification_level
del transform_content_filter
del transform_permissions
del transform_snowfalke
del transform_color
del transform_user
del transform_channel
del transform_overwrites
del transform_int__slowmode
del transform_avatar

class AuditLogChange(object):
    __slots__=('before', 'after', 'attr',)
    
    def __repr__(self):
        return f'{self.__class__.__name__}(attr=`{self.attr}`, before=`{self.before}`, after=`{self.after}`)'
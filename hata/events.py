# -*- coding: utf-8 -*-
__all__ = ('CommandProcesser', 'ContentParser', 'Cooldown',
    'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING', 'GUI_STATE_READY',
    'GUI_STATE_SWITCHING_CTX', 'GUI_STATE_SWITCHING_PAGE', 'Pagination',
    'ReactionAddWaitfor', 'ReactionDeleteWaitfor', 'multievent',
    'prefix_by_guild', 'wait_and_continue', 'wait_for_message',
    'wait_for_reaction', )

import re
from weakref import WeakKeyDictionary

from .futures import Task, sleep, PENDING

from .others import USER_MENTION_RP
from .parsers import check_passed,EventHandlerBase,EventDescriptor,compare_converted,check_name
from .emoji import BUILTIN_EMOJIS
from .exceptions import DiscordException
from .client_core import KOKORO

#Invite this as well, to shortcut imports
from .events_compiler import ContentParser

class asynclist(list):
    async def __call__(self,*args):
        for func in reversed(self):
            await func(*args)

COMMAND_RP=re.compile(' *([^ \t\\n]*) *(.*)')

#example
class CommandProcesser(EventHandlerBase):
    __slots__=('commands', 'default_event', 'ignorecase', 'invalid_command',
        'mention_prefix', 'prefix', 'prefixfilter', 'waitfors',)
    __event_name__='message_create'
    def __init__(self,prefix,ignorecase=True,mention_prefix=True):
        self.default_event=EventDescriptor.default_event
        self.invalid_command=EventDescriptor.default_event
        self.mention_prefix=mention_prefix
        self.waitfors=WeakKeyDictionary()
        self.commands={}
        self.update_prefix(prefix,ignorecase)
        self.ignorecase=ignorecase
        
    def update_prefix(self,prefix,ignorecase=None):
        if ignorecase is None:
            ignorecase=self.ignorecase
        if ignorecase:
            flag=re.I
        else:
            flag=0
        
        while True:
            if callable(prefix):
                def prefixfilter(message):
                    practical_prefix=prefix(message)
                    if re.match(re.escape(practical_prefix),message.content,flag) is None:
                        return
                    result=COMMAND_RP.match(message.content,len(practical_prefix))
                    if result is None:
                        return
                    return result.groups()
                
                break
            
            if type(prefix) is str:
                PREFIX_RP=re.compile(re.escape(prefix))
            elif isinstance(prefix,(list,tuple)):
                PREFIX_RP=re.compile("|".join(re.escape(p) for p in prefix))
            else:
                raise TypeError(f'Prefix can be only callable, str or tuple/list type, got {prefix!r}')
            
            def prefixfilter(message):
                result=PREFIX_RP.match(message.content)
                if result is None:
                    return
                result=COMMAND_RP.match(message.content,result.end())
                if result is None:
                    return
                return result.groups()
            
            break
        
        self.prefix=prefix
        self.prefixfilter=prefixfilter
        self.ignorecase=ignorecase

    def __setevent__(self,func,case):
        #called every time, but only if every other fails
        if case=='default_event':
            func=check_passed(func,2,'\'default_event\' expects 2 arguments (client, message).')
            self.default_event=func
        #called when user used bad command after the preset prefix, called if a command fails
        elif case=='invalid_command':
            func=check_passed(func,4,'\'invalid_command\' expected 4 arguemnts (client, message, command, content).')
            self.invalid_command=func
        else:
            #called first
            func=check_passed(func,3)
            self.commands[case]=func
        return func
    
    def __delevent__(self,func,case):
        if case=='default_event':
            if func is self.default_event:
                self.default_event=EventDescriptor.default_event
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) is not the same as the already loaded one: {self.default_event!r}')
        
        elif case=='invalid_command':
            if func is self.invalid_command:
                self.invalid_command=EventDescriptor.default_event
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) is not the same as the already loaded one: {self.invalid_command!r}')
        
        else:
            try:
                actual=self.commands[case]
            except KeyError as err:
                raise ValueError(f'The passed \'{case}\' is not added as a command right now.')
            
            if compare_converted(actual,func):
                del self.commands[case]
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) command is not the same as the already loaded one: {actual!r}')
            
    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(event(message,),client.loop)
            else:
                Task(event(message,),client.loop)
        
        if message.author.is_bot:
            return
        
        if not message.channel.cached_permissions_for(client).can_send_messages:
            return
        
        result=self.prefixfilter(message)
        
        if result is None:
            #start goto if needed
            while self.mention_prefix and (message.mentions is not None) and (client in message.mentions):
                result=USER_MENTION_RP.match(message.content)
                if result is None or int(result.group(1))!=client.id:
                    break
                result=COMMAND_RP.match(message.content,result.end())
                if result is None:
                    break
                
                command,content=result.groups()
                command=command.lower()
                
                try:
                    event=self.commands[command]
                except KeyError:
                    break
                return (await event(client,message,content))
        
        else:
            command,content=result
            command=command.lower()
            
            try:
                event=self.commands[command]
            except KeyError:
                return (await self.invalid_command(client,message,command,content))
            else:
                return (await event(client,message,content))
        
        return (await self.default_event(client,message))
            
    def append(self,wrapper,target):
        try:
            actual=self.waitfors[target]
            if type(actual) is asynclist:
                actual.append(wrapper)
            else:
                self.waitfors[target]=container=asynclist()
                container.append(actual)
                container.append(wrapper)
        except KeyError:
            self.waitfors[target]=wrapper

    def remove(self,wrapper,target,):
        try:
            container=self.waitfors.pop(target)
            if type(container) is asynclist:
                container.remove(wrapper)
                if len(container)==1:
                    self.waitfors[target]=container[0]
                else:
                    self.waitfors[target]=container
        except (KeyError,ValueError):
            #`KeyError` if `target` is missing
            #`ValueError` if `wrapper` is missing
            pass
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' prefix=', self.prefix.__repr__(),
            ', command count=', self.commands.__len__().__repr__(),
            ', mention_prefix=', self.mention_prefix.__repr__(),
                ]
        
        default_event=self.default_event
        if default_event is not EventDescriptor.default_event:
            result.append(', default_event=')
            result.append(default_event.__repr__())
        
        invalid_command=self.invalid_command
        if invalid_command is not EventDescriptor.default_event:
            result.append(', invalid_command=')
            result.append(invalid_command.__repr__())
        
        result.append('>')
        
        return ''.join(result)
        
class ReactionAddWaitfor(EventHandlerBase):
    __slots__=('waitfors',)
    __event_name__='reaction_add'
    
    def __init__(self):
        self.waitfors=WeakKeyDictionary()
    
    append=CommandProcesser.append
    remove=CommandProcesser.remove
    
    async def __call__(self,client,message,emoji,user):
        try:
            event=self.waitfors[message]
        except KeyError:
            return

        if type(event) is asynclist:
            for event in event:
                Task(event(emoji,user,),client.loop)
        else:
            Task(event(emoji,user,),client.loop)
            
class ReactionDeleteWaitfor(EventHandlerBase):
    __slots__=('waitfors',)
    __event_name__='reaction_delete'
    
    def __init__(self):
        self.waitfors=WeakKeyDictionary()
    
    append  = ReactionAddWaitfor.append
    remove  = ReactionAddWaitfor.remove
    __call__= ReactionAddWaitfor.__call__

#if target is message, we wait for emoji
#at the case of channel we wait for message

class multievent(object):
    __slots__=('events',)
    
    def __init__(self,*events):
        self.events=events
        
    def append(self,wrapper,target):
        for event in self.events:
            event.append(wrapper,target)
    
    def remove(self,wrapper,target):
        for event in self.events:
            event.remove(wrapper,target)

class waitfor_wrapper(object):
    __slots__=('client', 'event', 'feature', 'target', 'timeout', 'waiter',)
    #feature should be a class, with __init__ and **coro** __call__ magic methods
    def __init__(self,client,feature,timeout,event,target,):
        self.client=client
        self.feature=feature
        self.timeout=timeout
        self.waiter=None
        
        self.event=event
        self.target=target
        event.append(self,target)
        
        Task(self.run(),client.loop)
        
    async def run(self):
        loop=self.client.loop
        exception=None
        try:
            while self.timeout:
                #we check for new timeout every time, if u wanna extend it
                timeout=self.timeout
                self.timeout=0.
                self.waiter=sleep(timeout,loop)
                await self.waiter
            exception=TimeoutError()
        except BaseException as err:
            self.waiter=None
            #if anything happens we notify the client
            await self.client.events.error(self.client,f'{self.__class__.__name__}.run; block: try',err)
            exception=err
            #on failure/timeout we cancel the event
        finally:
            self.waiter=None
            self.event.remove(self,self.target)
            cancel=self.feature.cancel
            if cancel is not None:
                self.feature.cancel=None
                try:
                    await cancel(self.feature,self,exception)
                except BaseException as err:
                    await self.client.events.error(self.client,f'{self.__class__.__name__}.run; block: finally',err)
    
    def __call__(self,*args):
        #we just return, it will be awaited
        return self.feature(self,*args)
    
    def cancel(self):
        self.timeout=0.
        if self.waiter is not None:
            self.waiter.cancel_handles()
            self.waiter.set_result(None)
            self.waiter=None
            
#classes should be passed.
#they should implement:
#    __init__ (self,...) |CORO|
#    __call__(self,emoji,user) |CORO|
#    cancel(obj,wrapper,exception=None) |CORO| !or None! (Not method!)
#
#`start` is gets called when called as early as it gets space on the asyncloop
#If init fails the event gets cleaned up form the waitfors, then
#`cancel` will be called if applicable
#
#If we get any emojis at the message, `call` gets called. If u wait only on 1
#good reaction, u can call instantly `wrapper.cancel` to start the cleanup
#
#`wrapper.cancel` calls the event's `cancel` if applicable, then removes the
#event from the waitfors
#
#If any errors happen at `cancel`, it will show up on `client.events.error`,
#because "Errors should never pass silently"
#
#If you set timeout to 0 will trigger autoclose, so dont do it.
#
#If you want to extend the timeout, you can modify `wrapper.timeout` to the given
#value. When the current timeout ends, it will pickup the new one.
#
#
#on exception calls: "client.events.error"

GUI_STATE_READY          = 0
GUI_STATE_SWITCHING_PAGE = 1
GUI_STATE_CANCELLING     = 2
GUI_STATE_CANCELLED      = 3
GUI_STATE_SWITCHING_CTX  = 4


class Pagination(object):
    LEFT2   = BUILTIN_EMOJIS['track_previous']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['track_next']
    CROSS   = BUILTIN_EMOJIS['x']
    EMOJIS  = (LEFT2,LEFT,RIGHT,RIGHT2,CROSS,)
    
    __slots__=('cancel', 'channel', 'page', 'pages', 'task_flag',)
    async def __new__(cls,client,channel,pages,timeout=240.,message=None):
        self=object.__new__(cls)
        self.pages=pages
        self.page=0
        self.channel=channel
        self.cancel=cls._cancel
        self.task_flag=GUI_STATE_READY

        if message is None:
            message = await client.message_create(channel,embed=pages[0])

        if not channel.cached_permissions_for(client).can_add_reactions:
            return self

        message.weakrefer()
        if len(self.pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CROSS)

        waitfor_wrapper(client,self,timeout,multievent(client.events.reaction_add,client.events.reaction_delete),message,)
        return self
    
    async def __call__(self,wrapper,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return
        
        client=wrapper.client
        message=wrapper.target
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages
        
        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CROSS:
                    task_flag=GUI_STATE_CANCELLING
                return

            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            if emoji is self.RIGHT:
                page=self.page+1
                break
            if emoji is self.CROSS:
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                return wrapper.cancel()
            if emoji is self.LEFT2:
                page=0
                break
            if emoji is self.RIGHT2:
                page=len(self.pages)-1
                break
            return
        
        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(message,embed=self.pages[page])
        except DiscordException:
            self.task_flag=GUI_STATE_CANCELLED
            return wrapper.cancel()
        else:
            if self.task_flag==GUI_STATE_CANCELLING:
                self.task_flag=GUI_STATE_CANCELLED
                if can_manage_messages:
                    try:
                        await client.message_delete(message)
                    except DiscordException:
                        pass
                return wrapper.cancel()
            else:
                self.task_flag=GUI_STATE_READY

        if wrapper.timeout<240.:
            wrapper.timeout+=30.
            
    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass
    
    @staticmethod
    async def _cancel(self,wrapper,exception):
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag=GUI_STATE_CANCELLED
        if exception is None:
            return
        if isinstance(exception,TimeoutError):
            client=wrapper.client
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(wrapper.target)
                except DiscordException:
                    pass
            return
        #we do nothing
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' pages=', self.pages.__len__().__repr__(),
            ', page=', self.page.__repr__(),
            ', channel=', self.channel.__repr__(),
            ', task_flag='
                ]
        
        task_flag=self.task_flag
        result.append(task_flag.__repr__())
        result.append(' (')
        
        task_flag_name = (
            'GUI_STATE_READY',
            'GUI_STATE_SWITCHING_PAGE',
            'GUI_STATE_CANCELLING',
            'GUI_STATE_CANCELLED',
            'GUI_STATE_SWITCHING_CTX',
                )[task_flag]
        
        result.append(task_flag_name)
        result.append(')>')
        
        return ''.join(result)
        
class wait_and_continue(object):
    __slots__=('cancel', 'case', 'event', 'future',)
    def __init__(self,client,future,case,target,event,timeout):
        self.cancel=type(self)._default_cancel
        self.future=future
        self.case=case
        self.event=event
        
        waitfor_wrapper(client,self,timeout,event,target,)
        
    async def __call__(self,wrapper,*args):
        result=self.case(*args)
        if type(result) is bool:
            if result:
                if len(args)==1:
                    self.future.set_result_if_pending(args[0],)
                else:
                    self.future.set_result_if_pending(args,)
                
                wrapper.cancel()
        else:
            args=(*args,result,)
            self.future.set_result_if_pending(args,)
            
            wrapper.cancel()

    async def _default_cancel(self,wrapper,exception):
        future=self.future
        if future._state is PENDING:
            if exception is None:
                future.cancel()
            else:
                future.set_exception_if_pending(exception)
            #we do nothing


async def wait_for_reaction(client,message,case,timeout):
    future=client.loop.create_future()
    wait_and_continue(client,future,case,message,client.events.reaction_add,timeout)
    return (await future)

async def wait_for_message(client,channel,case,timeout):
    future=client.loop.create_future()
    wait_and_continue(client,future,case,channel,client.events.message_create,timeout)
    return (await future)

class prefix_by_guild(dict):
    __slots__=('default', 'orm',)
    
    def __init__(self,default,*orm):
        if type(default) is not str:
            raise TypeError (f'Default expected type str, got type {default.__class__.__name__}')
        self.default=default
        if orm:
            if len(orm)!=3:
                raise TypeError(f'Expected \'engine\', \'table\', \'model\' for orm, but got {len(orm)} elements')
            self.orm=orm
            Task(self._load_orm(),KOKORO)
            KOKORO.wakeup()
                
    def __call__(self,message):
        guild=message.guild
        if guild is not None:
            return self.get(guild.id,self.default)
        return self.default
    
    def __getstate__(self):
        return self.default
    def __setstate__(self,state):
        self.default=state
        self.orm=None
    
    def add(self,guild,prefix):
        guild_id=guild.id
        if guild_id in self:
            if prefix==self.default:
                del self[guild_id]
                if self.orm is not None:
                    Task(self._remove_prefix(guild_id),KOKORO)
                    KOKORO.wakeup()
                return True
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._modify_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
        else:
            if prefix==self.default:
                return False
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._add_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
    
    def to_json_serializable(self):
        result=dict(self)
        result['default']=self.default
        return result
    
    @classmethod
    def from_json_serialization(cls,data):
        self=dict.__new__(cls)
        self.default=data.pop('default')
        for id_,prefix in data.items():
            self[int(id_)]=prefix
        self.orm=None
        return self
    
    async def _load_orm(self,):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            result = await connector.execute(table.select())
            prefixes = await result.fetchall()
            for item in prefixes:
                self[item.guild_id]=item.prefix
    
    async def _add_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.insert(). \
                values(guild_id=guild_id,prefix=prefix))
    
    async def _modify_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.update(). \
                values(prefix=prefix). \
                where(model.guild_id==guild_id))
    
    async def _remove_prefix(self,guild_id):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.delete(). \
                where(model.guild_id==guild_id))

    def __repr__(self):
        return f'<{self.__class__.__name__} default=\'{self.default}\' len={self.__len__()}>'
    
    # because it is a builtin subclass, it will have __str__, so we overwrite that as well
    __str__=__repr__
    
class _CD_unit(object):
    __slots__=('expires_at', 'uses_left',)
    def __init__(self,expires_at,uses_left):
        self.expires_at=expires_at
        self.uses_left=uses_left
    
    def __repr__(self):
        return f'{self.__class__.__name__}(expires_at={self.expires_at}, uses_left={self.uses_left})'
    
class Cooldown(object):
    __async_call__=True
    
    __slots__=('__func__', '__name__', 'cache', 'checker', 'handler', 'limit',
        'reset', 'weight',)
    
    async def _default_handler(client,message,command,time_left):
        return
    
    def __new__(cls,for_,reset,limit=1,weight=1,handler=_default_handler,case=None,func=None):
        if 'user'.startswith(for_):
            checker=cls._check_user
        elif 'channel'.startswith(for_):
            checker=cls._check_channel
        elif 'guild'.startswith(for_):
            checker=cls._check_guild
        else:
            raise ValueError(f'\'for_\' can be \'user\', \'channel\' or \'guild\', got {for_!r}')
        
        self=object.__new__(cls)
        self.checker=checker
        self.handler=handler
        
        if type(reset) is not float:
            reset=float(reset)
        
        self.reset=reset
        
        self.cache={}
        
        if type(weight) is not int:
            weight=int(weight)
        self.weight=weight
        
        if type(limit) is not int:
            limit=int(limit)
        self.limit=limit-weight
        
        if func is None:
            if case is None:
                case=''
            self.__name__=case
            self.__func__=EventDescriptor.default_event
            return self._wrapper
        
        self.__name__=check_name(func,case)
        self.__func__=check_passed(func,3)
        return self

    def _wrapper(self,func):
        if not self.__name__:
            self.__name__=check_name(func,None)
        self.__func__=check_passed(func,3)
        return self
    
    def __call__(self,client,message,*args):
        loop=client.loop
        value=self.checker(self,message,loop)
        if value:
            return self.handler(client,message,self.__name__,value-loop.time())
        else:
            return self.__func__(client,message,*args)
    
    def shared(source,weight=0,case=None,func=None):
        self        = object.__new__(type(source))
        self.checker= source.checker
        self.reset  = source.reset
        self.cache  = source.cache
        if type(weight) is not int:
            weight=int(weight)
        if not weight:
            weight = source.weight
        self.weight = weight
        self.limit  = source.limit+source.weight-weight
        self.handler= source.handler
        
        if func is None:
            if case is None:
                case=''
            self.__name__=case
            self.__func__=EventDescriptor.default_event
            return self._wrapper
        
        self.__name__=check_name(func,case)
        self.__func__=check_passed(func,3)
    
    @staticmethod
    def _check_user(self,message,loop):
        id_=message.author.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
    
    @staticmethod
    def _check_channel(self,message,loop):
        id_=message.channel.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at

    #returns -1. if non guild
    @staticmethod
    def _check_guild(self,message,loop):
        channel=message.channel
        if channel.type in (1,3):
            return -1.
        else:
            id_=channel.guild.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at

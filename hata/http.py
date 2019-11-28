# -*- coding: utf-8 -*-
__all__ = ('DiscordHTTPClient', )
import sys, re
from .dereaddons_local import multidict_titled, modulize
from .futures import Future, sleep
from .py_url import URL

from .py_connector import TCPConnector
from .py_cookiejar import CookieJar
from .py_reqrep import ClientRequest,merge_ssl_params,Request_CM
from .py_helpers import TimeoutHandle,CeilTimeout,tcp_nodelay
from .py_hdrs import METH_PATCH, METH_GET, METH_DELETE, METH_POST, METH_PUT,\
    CONTENT_TYPE, USER_AGENT, AUTHORIZATION, METH_HEAD, CONTENT_LENGTH, URI,\
    LOCATION

from .exceptions import DiscordException
from .others import to_json, from_json, quote, Discord_hdrs

AUDIT_LOG_REASON    = Discord_hdrs.AUDIT_LOG_REASON
RATELIMIT_REMAINING = Discord_hdrs.RATELIMIT_REMAINING
RATELIMIT_PRECISION = Discord_hdrs.RATELIMIT_PRECISION

from .ratelimit import ratelimit_handler,ratelimit_global,GLOBALLY_LIMITED

#this file contains every link needed to communicate with discord
VALID_ICON_FORMATS   = ('jpg','jpeg','png','webp')
VALID_ICON_SIZES     = {1<<x for x in range(4,13)}
VALID_ICON_FORMATS_EXTENDED = (*VALID_ICON_FORMATS,'gif',)

API_ENDPOINT='https://discordapp.com/api/v7' #v7 includes special error messages
CDN_ENDPOINT='https://cdn.discordapp.com'
DIS_ENDPOINT='https://discordapp.com'

@modulize
class URLS:
    style_pattern=re.compile('(^shield$)|(^banner[1-4]$)')
    #returns a URL that allows the client to jump to this message
    #guild is guild's id, or @me if there is no guild
    def message_jump_url(message):
        channel=message.channel
        guild=channel.guild
        guild_id='@me' if guild is None else str(guild.id)
        return f'{DIS_ENDPOINT}/channels/{guild_id}/{channel.id}/{message.id}'

    def guild_icon_url(guild):
        icon=guild.icon
        if not icon:
            return None
        
        if guild.has_animated_icon:
            start='a_'
            ext='gif'
        else:
            start=''
            ext='png'

        return f'{CDN_ENDPOINT}/icons/{guild.id}/{start}{icon:0>32x}.{ext}'

    def guild_icon_url_as(guild,ext='png',size=None):
        icon=guild.icon
        if not icon:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if guild.has_animated_icon:
                start='a_'
                ext='gif'
            else:
                start=''
                ext='png'
        else:
            if guild.has_animated_icon:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
                start='a_'
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
                start=''
    
        return f'{CDN_ENDPOINT}/icons/{guild.id}/{start}{icon:0>32x}.{ext}{end}'

    def guild_splash_url(guild):
        splash=guild.splash
        if splash:
            return f'{CDN_ENDPOINT}/splashes/{guild.id}/{splash:0>32x}.png'
        return None
        
    def guild_splash_url_as(guild,ext='png',size=None):
        splash=guild.splash
        if not splash:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/splashes/{guild.id}/{splash:0>32x}.{ext}{end}'

    def guild_banner_url(guild):
        banner=guild.banner
        if not banner:
            return None
            
        return f'{CDN_ENDPOINT}/banners/{guild.id}/{banner:0>32x}.png'
    
    
    def guild_banner_url_as(guild,ext='png',size=None):
        banner=guild.banner
        if not banner:
            return None
        
        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/banners/{guild.id}/{banner:0>32x}.{ext}{end}'


    def guild_embed_url(guild,style='shield'):
        if URLS.style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        return f'{API_ENDPOINT}/guilds/{guild.id}/embed.png?style={style}'

    def guild_widget_url(guild,style='shield'):
        if URLS.style_pattern.match(style) is None:
            raise ValueError(f'Invalid style: {style!r}')
        return f'{API_ENDPOINT}/guilds/{guild.id}/widget.png?style={style}'

    def guild_widget_json_url(guild):
        return  f'{API_ENDPOINT}/guilds/{guild.id}/widget.json'

    def channel_group_icon_url(channel):
        icon=channel.icon
        if not icon:
            return None
        
        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{icon:0>32x}.png'
        
    def channel_group_icon_url_as(channel,ext='png',size=None):
        icon=channel.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/channel-icons/{channel.id}/{icon:0>32x}.{ext}{end}'

    def emoji_url(emoji):
        if emoji.is_unicode_emoji():
            return None
        
        if emoji.animated:
             ext='gif'
        else:
             ext='png'
            
        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}'

    def emoji_url_as(emoji,ext=None,size=None):
        if emoji.is_unicode_emoji():
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if emoji.animated:
                ext='gif'
            else:
                ext='png'
        else:
            if emoji.animated:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
            else:
                if ext not in VALID_ICON_FORMATS:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/emojis/{emoji.id}.{ext}{end}'

    def webhook_url(webhook):
        return f'{API_ENDPOINT}/webhooks/{webhook.id}/{webhook.token}'

    webhook_urlpattern=re.compile('discordapp.com/api/webhooks/(?P<id>[0-9]{17,21})/(?P<token>[A-Za-z0-9\.\-\_]{60,68})')

    def webhook_avatar_url(webhook):
        avatar=webhook.avatar
        if not avatar:
            #default avatar
            return '{CDN_ENDPOINT}/embed/avatars/0.png'
            
        return f'{CDN_ENDPOINT}/avatars/{webhook.id}/{avatar:0>32x}.png'
        
    def webhook_avatar_url_as(webhook,ext='png',size=None):
        avatar=webhook.avatar
        if not avatar:
            #default avatar
            return '{CDN_ENDPOINT}/embed/avatars/0.png'

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
        
        return f'{CDN_ENDPOINT}/avatars/{webhook.id}/{avatar:0>32x}.{ext}{end}'

    def invite_url(invite):
        return f'http://discord.gg/{invite.code}'

    def activity_asset_image_large_url(activity):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.png'


    def activity_asset_image_large_url_as(activity,ext='png',size=None):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_large=activity.asset_image_large
        if not asset_image_large:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_large}.{ext}{end}'
        
    def activity_asset_image_small_url(activity):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.png'

    def activity_asset_image_small_url_as(activity,ext='png',size=None):
        application_id=activity.application_id
        if not application_id:
            return None

        asset_image_small=activity.asset_image_small
        if not asset_image_small:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
        
        return f'{CDN_ENDPOINT}/app-assets/{application_id}/{asset_image_small}.png'

    def user_avatar_url(user):
        avatar=user.avatar
        if not avatar:
            return user.default_avatar.url
        
        if user.has_animated_avatar:
            start='a_'
            ext='gif'
        else:
            start=''
            ext='png'

        return f'{CDN_ENDPOINT}/avatars/{user.id}/{start}{avatar:0>32x}.{ext}'

    def user_avatar_url_as(user,ext=None,size=None):
        avatar=user.avatar
        if not avatar:
            return user.default_avatar.url

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')
        
        if ext is None:
            if user.has_animated_avatar:
                start='a_'
                ext='gif'
            else:
                start=''
                ext='png'
        else:
            if user.has_animated_avatar:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS_EXTENDED}, and not {ext}.')
                start='a_'
            else:
                if ext not in VALID_ICON_FORMATS_EXTENDED:
                    raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')
                start=''

        return f'{CDN_ENDPOINT}/avatars/{user.id}/{start}{avatar:0>32x}.{ext}{end}'

    def default_avatar_url(default_avatar):
        return f'{CDN_ENDPOINT}/embed/avatars/{default_avatar.value}.png'

    def application_icon_url(application):
        icon=application.icon
        if not icon:
            return None
            
        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{icon:0>32x}.png'
        
        
    def application_icon_url_as(application,ext='png',size=None):
        icon=application.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-icons/{application.id}/{icon:0>32x}.{ext}{end}'

    def team_icon_url(team):
        icon=team.icon
        if not icon:
            return None
        
        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{icon:0>32x}.png'
        
    def team_icon_url_as(team,ext='png',size=None):
        icon=team.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/team-icons/{team.id}/{icon:0>32x}.{ext}{end}'

    def achievement_icon_url(achievement):
        icon=achievement.icon
        if not icon:
            return None
            
        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{icon:0>32x}.png'
        

    def achievement_icon_url_as(achievement,ext='png',size=None):
        icon=achievement.icon
        if not icon:
            return None

        if size is None:
            end=''
        elif size in VALID_ICON_SIZES:
            end=f'?size={size}'
        else:
            raise ValueError(f'Size must be power of 2 between 16 and 4096 and not: {size}.')

        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Extension must be one of {VALID_ICON_FORMATS}, and not {ext}.')

        return f'{CDN_ENDPOINT}/app-assets/{achievement.application_id}/achievements/{achievement.id}/icons/{icon:0>32x}.{ext}{end}'


DEFAULT_TIMEOUT=20.

implement=sys.implementation
version_l=['Discordclient (HuyaneMatsu) Python (',implement.name,' ',str(implement.version[0]),'.',str(implement.version[1]),' ']
if implement.version[3]!='final':
    version_l.append(implement.version[3])
version_l.append(')')
USER_AGENT=''.join(version_l)

del implement
del version_l

del sys

class DiscordHTTPClient(object):
    __slots__=('connector', 'cookie_jar', 'global_lock', 'header', 'locks',
        'loop', 'proxy_auth', 'proxy_url',)
    def __init__(self,client,proxy_url=None,proxy_auth=None):
        self.header=multidict_titled()
        self.header[USER_AGENT]=USER_AGENT
        self.header[AUTHORIZATION]=f'Bot {client.token}' if client.is_bot else client.token
        self.header[RATELIMIT_PRECISION]='millisecond'

        loop            = client.loop
        self.loop       = loop
        
        self.connector  = TCPConnector(loop)
        self.cookie_jar = CookieJar(loop)

        self.proxy_url  = proxy_url
        self.proxy_auth = proxy_auth
        
        self.global_lock= None
        self.locks      = {}

    @classmethod
    def unbound(cls,loop,proxy_url=None,proxy_auth=None):
        self=object.__new__(cls)

        self.header     = multidict_titled()
        self.loop       = loop

        self.connector  = TCPConnector(loop)
        self.cookie_jar = CookieJar(loop)

        self.proxy_url  = proxy_url
        self.proxy_auth = proxy_auth

        self.global_lock= None #placeholder
        self.locks      = {}   #placeholder

        return self

    async def request(self,handler,method,url,data=None,params=None,header=None,reason=None):

        if header is None:
            #normal request
            header=self.header.copy()

            if type(data) in (dict,list):
                header[CONTENT_TYPE]='application/json'
                data=to_json(data)

            if reason is not None:
                header[AUDIT_LOG_REASON]=quote(reason)
        else:
            #bearer or webhook request
            if type(data) in (dict,list) and CONTENT_TYPE not in header:
                header[CONTENT_TYPE]='application/json'
                data=to_json(data)
            
        #handling rateimit
        if self.global_lock is not None:
            await self.global_lock

        if handler.group_id:
            try:
                old_handler=self.locks[handler]
            except KeyError:
                self.locks[handler]=handler
            else:
                self.locks[handler]=handler
                if old_handler.is_active():
                    await old_handler

        with handler:
            try_again=4
            while True:
                try:
                    async with Request_CM(self._request(method,url,header,data,params)) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if try_again:
                        #os cant handle more, need to wait for the blocking job to be done
                        await sleep(.5/try_again,self.loop)
                        #invalid adress causes OSError too, but we will let it run 5 times, then raise a ConnectionError
                        try_again-=1
                        continue
                    raise ConnectionError('Invalid adress') from err
                headers=response.headers
                status=response.status
                
                if headers[CONTENT_TYPE]=='application/json':
                    response_data=from_json(response_data)
                
                if 199<status<305:
                    if headers.get(RATELIMIT_REMAINING,'1')=='0':
                        handler.set_delay(headers)
                    return response_data
                
                if status==429:
                    retry_after=response_data['retry_after']/1000.
                    if response_data['global']:
                        await ratelimit_global(self,retry_after)
                    else:
                        await sleep(retry_after,self.loop)
                    continue
                
                if (status==500 or status==502) and try_again:
                    await sleep(10./try_again,self.loop)
                    try_again-=1
                    continue
                
                raise DiscordException(response,response_data)


    async def _request(self,method,url,headers,data=None,params=None,redirect=3):
        history         = []
        url             = URL(url)
        proxy_url       = self.proxy_url
        timer_obj       = TimeoutHandle(self.loop,DEFAULT_TIMEOUT)
        timer_handler   = timer_obj.start()
        timer           = timer_obj.timer()
        
        try:
            with timer:
                while True:
                    cookies=self.cookie_jar.filter_cookies(url)

                    if proxy_url:
                        proxy_url=URL(proxy_url)
            
                    request=ClientRequest(method,url,self.loop,headers,data,params,
                        cookies,None,proxy_url,self.proxy_auth,timer)

                    with CeilTimeout(self.loop,DEFAULT_TIMEOUT):
                        connection = await self.connector.connect(request,DEFAULT_TIMEOUT)

                    tcp_nodelay(connection.transport,True)

                    connection.protocol.set_response_params(
                        timer=timer,
                        skip_payload=method.upper()=='HEAD',
                        read_until_eof=True,
                        auto_decompress=True,
                        read_timeout=None)
                    
                    try:
                        response=await request.send(connection)
                        try:
                            await response.start(connection)
                        except BaseException:
                            response.close()
                            raise
                    except BaseException:
                        connection.close()
                        raise

                    #we do nothing with os error

                    self.cookie_jar.update_cookies(response.cookies,response.url)

                    # redirects
                    if response.status in (301,302,303,307) and redirect:
                        redirect-=1
                        history.append(response)
                        if not redirect:
                            response.close()
                            raise ConnectionError('Too many redirects',history[0].request_info,tuple(history))

                        # For 301 and 302, mimic IE behaviour, now changed in RFC.
                        # Details: https://github.com/kennethreitz/requests/pull/269
                        if (response.status==303 and response.method!=METH_HEAD) \
                           or (response.status in (301,302) and response.method==METH_POST):
                            method=METH_GET
                            data=None
                            headers.pop(CONTENT_LENGTH,None)

                        redirect_url = (response.headers.get(LOCATION) or response.headers.get(URI))
                        if redirect_url is None:
                            break
                        else:
                            response.release()
                        
                        redirect_url=URL(redirect_url)

                        scheme=redirect_url.scheme
                        if scheme not in ('http','https',''):
                            response.close()
                            raise ValueError('Can redirect only to http or https')
                        elif not scheme:
                            redirect_url=url.join(redirect_url)


                        if url.origin()!=redirect_url.origin():
                            headers.pop(AUTHORIZATION,None)
                            
                        url=redirect_url
                        params = None
                        response.release()
                        continue

                    break

            # register connection
            if response.connection is None:
                timer_handler.cancel()
            else:
                response.connection.add_callback(timer_handler.cancel)

            response.history=tuple(history)
            return response
        except BaseException:
            timer_obj.close()
            raise
        
    async def _request2(self,method,url,headers=None,params=None,data=None,
            auth=None,redirects=10,read_until_eof=True,proxy_url=None, proxy_auth=None,timeout=DEFAULT_TIMEOUT,
            ssl=None,verify_ssl=None,ssl_context=None,fingerprint=None,):

        # Merge with default headers and transform to multidict_titled
        headers = multidict_titled(headers)

        if (headers and auth is not None and AUTHORIZATION in headers):
            raise ValueError('Can\'t combine \'Authorization\' header with \'auth\' argument')

        if not proxy_url and self.proxy_url:
            proxy_url   = self.proxy_url
        ssl             = merge_ssl_params(ssl,verify_ssl,ssl_context,fingerprint)
        history         = []
        url             = URL(url)
        timer_obj       = TimeoutHandle(self.loop,timeout)
        timer_handler   = timer_obj.start()
        timer           = timer_obj.timer()

        try:
            with timer:
                while True:
                    cookies=self.cookie_jar.filter_cookies(url)

                    if proxy_url:
                        proxy_url=URL(proxy_url)

                    request=ClientRequest(method,url,self.loop,headers,data,params,
                        cookies,auth,proxy_url,self.proxy_auth,timer,ssl)
                    
                    with CeilTimeout(self.loop,timeout):
                        connection=await self.connector.connect(request,timeout)

                    tcp_nodelay(connection.transport,True)

                    connection.protocol.set_response_params(
                        timer=timer,
                        skip_payload=method.upper()=='HEAD',
                        read_until_eof=read_until_eof,
                        auto_decompress=True,
                        read_timeout=None)

                    try:
                        response=await request.send(connection)
                        try:
                            await response.start(connection)
                        except BaseException:
                            response.close()
                            raise
                    except BaseException:
                        connection.close()
                        raise
 
                    #we do nothing with os error

                    self.cookie_jar.update_cookies(response.cookies,response.url)

                    # redirects
                    if response.status in (301,302,303,307) and redirects:
                        redirects-=1
                        history.append(response)
                        if not redirects:
                            response.close()
                            raise ConnectionError('Too many redirects',history[0].request_info,tuple(history))

                        # For 301 and 302, mimic IE behaviour, now changed in RFC.
                        # Details: https://github.com/kennethreitz/requests/pull/269
                        if (response.status==303 and response.method!=METH_HEAD) \
                                or (response.status in (301, 302) and response.method==METH_POST):
                            
                            method=METH_GET
                            data=None
                            content_ln=headers.get(CONTENT_LENGTH)
                            if (content_ln is not None) and content_ln:
                                del headers[CONTENT_LENGTH]

                        redirect_url = response.headers.get(LOCATION)
                        if redirect_url is None:
                            redirect_url = response.headers.get(URI)
                            if redirect_url is None:
                                break
                        
                        response.release()
                        
                        redirect_url=URL(redirect_url)

                        scheme=redirect_url.scheme
                        if scheme not in ('http', 'https', ''):
                            response.close()
                            raise ValueError('Can redirect only to http or https')
                        elif not scheme:
                            redirect_url=url.join(redirect_url)

                        url     = redirect_url
                        params  = None
                        await response.release()
                        continue

                    break
            
            # register connection
            if response.connection is not None:
                response.connection.add_callback(timer_handler.cancel)
            else:
                timer_handler.cancel()
            
            response.history=tuple(history)
            return response
        
        except BaseException:
            timer_obj.close()
            raise
    
    def close(self):
        connector=self.connector
        if connector is not None:
            if not connector.closed:
                connector.close()
            self.connector=None

        result=Future(self.loop)
        result.set_result(None)
        return result
        
    def restart(self):
        connector=self.connector
        if (connector is not None) and (not connector.closed):
            connector.close()
        
        self.connector=TCPConnector(self.loop)

        result=Future(self.loop)
        result.set_result(None)
        return result
    
    @property
    def closed(self):
        connector=self.connector
        return (connector is None) or connector.closed
        
    async def __aenter__(self):
        return self

    async def __aexit__(self,exc_type,exc_val,exc_tb):
        await self.close()

    def __del__(self):
        if self.connector is None:
            return
        if not self.connector.closed:
            self.connector.close()
        
        self.connector=None
    
    def request_(self,meth,url,headers=None,**kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(meth,url,headers,**kwargs))

    def request_get(self,url):
        return Request_CM(self._request(METH_GET,url,multidict_titled()))

    #client
    
    def client_edit(self,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,59136),METH_PATCH,
            f'{API_ENDPOINT}/users/@me',data)

    def client_edit_nick(self,guild_id,data,reason):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,48384),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick',data,reason=reason)

    def client_user(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me')

    #hooman only
    def client_get_settings(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/settings')
    
    #hooman only
    def client_edit_settings(self,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/users/@me/settings',data=data)

    def client_logout(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/auth/logout')

    def guild_get_all(self,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,62720),METH_GET,
            f'{API_ENDPOINT}/users/@me/guilds',params=data)

    def channel_private_get_all(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/channels')

    #hooman only
    def client_gateway_hooman(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/gateway')

    #bot only
    def client_gateway_bot(self):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,41216),METH_GET,
            f'{API_ENDPOINT}/gateway/bot')
    
    #bot only
    def client_application_info(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/oauth2/applications/@me')

    def client_connections(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/connections')

    #oauth2
    
    def oauth2_token(self,data): #UNLIMITED
        header=multidict_titled()
        dict.__setitem__(header,CONTENT_TYPE,['application/x-www-form-urlencoded'])
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{DIS_ENDPOINT}/api/oauth2/token',data,header=header)
    
    def user_info(self,header):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me',header=header)
    

    def user_connections(self,header):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/@me/connections',header=header)

    def guild_user_add(self,guild_id,user_id,data):
        return self.request(ratelimit_handler(self.loop,guild_id,53760),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data)
        
    def user_guilds(self,header):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,60928),METH_GET,
            f'{API_ENDPOINT}/users/@me/guilds',header=header)
    
    #channel
    def channel_private_create(self,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/@me/channels',data)

    def channel_group_create(self,user_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/{user_id}/channels',data)        

    def channel_group_leave(self,channel_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}')

    def channel_group_user_add(self,channel_id,user_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')

    def channel_group_user_delete(self,channel_id,user_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/recipients/{user_id}')

    def channel_group_edit(self,channel_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',data)

    #found in discord.py rewrite, dunno what it does, could not even find
    #so the http wont even get this feature
    #def channel_group_convert(self,channel_id):
    #    return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
    #        f'{API_ENDPOINT}/channels/{channel_id}/convert')
    
    def channel_move(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',data,reason=reason)

    def channel_edit(self,channel_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}',data,reason=reason)

    def channel_create(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels',data,reason=reason)

    def channel_delete(self,channel_id,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}',reason=reason)

    def channel_follow(self,channel_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/followers',data)

    def permission_ow_create(self,channel_id,overwrite_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',data,reason=reason)

    def permission_ow_delete(self,channel_id,overwrite_id,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',reason=reason)

    #messages

    #hooman only
    def message_mar(self,channel_id,message_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/ack',data)

    def message_get(self,channel_id,message_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}')

    def message_logs(self,channel_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',params=data)

    def message_create(self,channel_id,data):
        return self.request(ratelimit_handler(self.loop,channel_id,28672),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages',data)

    async def message_delete(self,channel_id,message_id,reason):
        try:
            result = await self.request(ratelimit_handler(self.loop,channel_id,71680),METH_DELETE,
                f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',reason=reason)
            return result
        except DiscordException as err:
            if err.response.status==404: #404==already deleted message
                return
            raise
            
    def message_delete_multiple(self,channel_id,data,reason):
        return self.request(ratelimit_handler(self.loop,channel_id,30464),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk_delete',data,reason=reason)

    def message_edit(self,channel_id,message_id,data):
        return self.request(ratelimit_handler(self.loop,channel_id,32256),METH_PATCH,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',data)

    def message_suppress_embeds(self,channel_id,message_id,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,73472),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds',data)

    def message_pin(self,channel_id,message_id):
        return self.request(ratelimit_handler(self.loop,channel_id,34048),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')

    def message_unpin(self,channel_id,message_id):
        return self.request(ratelimit_handler(self.loop,channel_id,34048),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}')

    def channel_pins(self,channel_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,35840),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/pins')

    #typing
    
    def typing(self,channel_id):
        return self.request(ratelimit_handler(self.loop,channel_id,37632),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/typing')

    #reactions

    def reaction_add(self,channel_id,message_id,reaction):
        return self.request(ratelimit_handler(self.loop,channel_id,26880),METH_PUT,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
            
    def reaction_delete(self,channel_id,message_id,reaction,user_id):
        return self.request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}')

    def reaction_delete_own(self,channel_id,message_id,reaction):
        return self.request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')

    def reaction_clear(self,channel_id,message_id):
        return self.request(ratelimit_handler(self.loop,channel_id,26880),METH_DELETE,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions')

    def reaction_users(self,channel_id,message_id,reaction,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',params=data)

    #guild
    
    def guild_get(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}')

    def guild_user_delete(self,guild_id,user_id,reason):
        return self.request(ratelimit_handler(self.loop,guild_id,50176),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',reason)

    def guild_ban_add(self,guild_id,user_id,data,reason):
        if reason:
            data['reason']=quote(reason)
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',params=data)

    def guild_ban_delete(self,guild_id,user_id,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',reason=reason)

    def user_edit(self,guild_id,user_id,data,reason):
        return self.request(ratelimit_handler(self.loop,guild_id,51968),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data,reason=reason)

    #hooman only
    def guild_mar(self,guild_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/ack',data)

    def guild_leave(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/users/@me/guilds/{guild_id}')

    def guild_delete(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}')

    def guild_create(self,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds',data)

    def guild_prune(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune',params=data,reason=reason)

    def guild_prune_estimate(self,guild_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/prune',params=data)

    def guild_edit(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}',data,reason=reason)

    def guild_bans(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans')

    def guild_ban_get(self,guild_id,user_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}')
    
    def vanity_get(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url')

    def vanity_edit(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url',data,reason=reason)

    def audit_logs(self,guild_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs',params=data)

    def user_role_add(self,guild_id,user_id,role_id,reason):
        return self.request(ratelimit_handler(self.loop,guild_id,55552),METH_PUT,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',reason=reason)

    def user_role_delete(self,guild_id,user_id,role_id,reason):
        return self.request(ratelimit_handler(self.loop,guild_id,55552),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',reason=reason)

    def user_move(self,guild_id,user_id,data):
        return self.request(ratelimit_handler(self.loop,guild_id,51968),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',data)

    def integration_get_all(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations')

    def integration_create(self,guild_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations',data)

    def integration_edit(self,guild_id,integration_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}',data)

    def integration_delete(self,guild_id,integration_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}')

    def integration_sync(self,guild_id,integration_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/integrations/{integration_id}/sync')

    def guild_embed_get(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed')

    def guild_embed_edit(self,guild_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/embed',data)

    def guild_widget_get(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/widget.json',header={})
    
    def guild_users(self,guild_id,data):
        return self.request(ratelimit_handler(self.loop,guild_id,68096),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members',params=data)

    def guild_regions(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/regions')

    def guild_channels(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/channels')

    def guild_roles(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles')

    #invite

    def invite_create(self,channel_id,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,39424),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/invites',data)
    
    def invite_get(self,invite_code,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,57344),METH_GET,
            f'{API_ENDPOINT}/invites/{invite_code}',params=data)

    def invite_get_guild(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/invites')
    
    def invite_get_channel(self,channel_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/invites')

    def invite_delete(self,invite_code,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/invites/{invite_code}',reason=reason)


    #role

    def role_edit(self,guild_id,role_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',data,reason=reason)

    def role_delete(self,guild_id,role_id,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',reason=reason)

    def role_create(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',data,reason=reason)

    def role_move(self,guild_id,data,reason):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/roles',data,reason=reason)

    #emoji

    def emoji_get(self,guild_id,emoji_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}')

    def guild_emojis(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis')
        
    def emoji_edit(self,guild_id,emoji_id,data,reason):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,46592),METH_PATCH,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',data,reason=reason)

    def emoji_create(self,guild_id,data,reason):
        return self.request(ratelimit_handler(self.loop,guild_id,43008),METH_POST,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis',data,reason=reason)

    def emoji_delete(self,guild_id,emoji_id,reason):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,44800),METH_DELETE,
            f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',reason=reason)

    #relations

    def relationship_delete(self,user_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}')

    def relationship_create(self,user_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PUT,
            f'{API_ENDPOINT}/users/@me/relationships/{user_id}',data)

    def relationship_friend_request(self,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/users/@me/relationships',data)

    #webhook
    
    def webhook_create(self,channel_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks',data)

    def webhook_get(self,webhook_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/webhooks/{webhook_id}')

    def webhook_get_channel(self,channel_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/channels/{channel_id}/webhooks')

    def webhook_get_guild(self,guild_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/webhooks')
    
    def webhook_get_token(self,webhook):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            webhook.url,header={})
    
    def webhook_delete_token(self,webhook):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            webhook.url,header={})

    def webhook_delete(self,webhook_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/webhooks/{webhook_id}')

    def webhook_edit_token(self,webhook,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            webhook.url,data,header={})

    def webhook_edit(self,webhook_id,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_PATCH,
            f'{API_ENDPOINT}/webhooks/{webhook_id}',data)

    def webhook_send(self,webhook,data,wait):
        return self.request(ratelimit_handler(self.loop,webhook.id,66304),METH_POST,
            f'{webhook.url}?wait={wait:d}',data,header={})
    
    #user

    def user_get(self,user_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,64512),METH_GET,
            f'{API_ENDPOINT}/users/{user_id}')

    def guild_user_get(self,guild_id,user_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,69888),METH_GET,
            f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}')
    
    #hooman only
    def user_profle(self,user_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/users/{user_id}/profile')


    #hypesquad

    def hypesquad_house_change(self,data):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_POST,
            f'{API_ENDPOINT}/hypesquad/online',data)

    def hypesquad_house_leave(self):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_DELETE,
            f'{API_ENDPOINT}/hypesquad/online')

    #achievements
    
    def achievement_get_all(self,application_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,75264),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements')

    def achievement_get(self,application_id,achievement_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,77056),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')

    def achievement_create(self,application_id,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,78848),METH_POST,
            f'{API_ENDPOINT}/applications/{application_id}/achievements',data)

    def achievement_edit(self,application_id,achievement_id,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,80640),METH_PATCH,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',data)

    def achievement_delete(self,application_id,achievement_id):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,82432),METH_DELETE,
            f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}')

    def user_achievements(self,application_id,header):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,84224),METH_GET,
            f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements',header=header)
    
    def user_achievement_update(self,user_id,application_id,achievement_id,data):
        return self.request(ratelimit_handler(self.loop,GLOBALLY_LIMITED,86016),METH_PUT,
            f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}',data)

    #random
    
    #hooman only sadly, but this would be nice to be allowed, to get name and icon at least
    def application_get(self,application_id):
        return self.request(ratelimit_handler.unlimited(self.loop),METH_GET,
            f'{API_ENDPOINT}/applications/{application_id}')

del re
del modulize
del Discord_hdrs

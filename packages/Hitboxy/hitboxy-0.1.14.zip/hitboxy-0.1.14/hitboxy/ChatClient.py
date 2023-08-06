import httplib
import random
import json
import time
import datetime
import logging

import websocket

from hitboxy import ApiClient

LOG = logging.getLogger(__name__)

class ConnectionFailedError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ChatClient(object):
    def __init__(self, username="UnknownSoldier", password=""):
        self.path = '/socket.io/1'

        self.username = username
        self.password = password
        self.name_color = 'ff0000'
        
        self.api = ApiClient()
        self.auth_token = None

    def _connect(self):
        self.servers = ApiClient.get_chat_servers()
        self.server = random.choice(self.servers)
        
        c = httplib.HTTPConnection(self.server)
        c.request("GET", self.path)
        r = c.getresponse()
        if r.status != 200:
            raise ConnectionFailedError('wrong status response from chat server: %s - %s' % (r.status, r.reason))            
        data = r.read()
        if not ':' in data:
            raise ConnectionFailedError("wrong response from chat server: '%s'" % (data))
        data = data.split(':')

        self.id = data[0]

        LOG.debug("choosen server: %s", self.server)
        LOG.debug("id: %s", self.id)

        #ws://<server>/socket.io/1/websocket/<id>
        wsurl = "ws://" + self.server + self.path + "/websocket/" + self.id

        websocket.setdefaulttimeout(10.0)
        self.socket = websocket.WebSocketApp(
            wsurl,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
        )
        self.socket.on_open = self.on_open
        self.socket.run_forever()

    def _send(self, data):
        self.socket.send(data)

    def _send_message(self, method, params):
        message = {
            'name': 'message',
            'args': [
                {
                    'method': method,
                    'params': params
                }
            ]
        }
        self._send('5:::' + json.dumps(message))

    def on_open(self, ws):
        print "on_open:", ws

    def on_close(self, ws):
        print "on_close:", ws

    def on_error(self, ws, error):
        print "on_error:", ws, error

    def on_message(self, ws, message):
        LOG.debug("on_message: %s", message)
        if message == '1::':
            if self.username != "UnknownSoldier":
                LOG.debug("aquiring auth token for user %s ...", self.username)
                self.auth_token = ApiClient.get_auth_token(self.username, self.password)
            self.on_login()
        elif message == '2::':
            self.socket.send('2::')
        elif message.startswith('5:::'):
            data = json.loads(message[4:])
            if data['name'] != 'message': return
            msg = json.loads(data['args'][0])
            self.on_system_message(msg['method'], msg['params'])      

    #--------------------------------------------------------------------------------------------------------------------------------
    #-- Events
    #--------------------------------------------------------------------------------------------------------------------------------
    def on_login(self):
        pass

    def on_channel_login(self, channel, name, role):
        pass

    def on_system_message(self, method, params):
        if method == 'loginMsg':
            self.on_channel_login(params['channel'], params['name'], params['role'])
        elif method == 'chatMsg':
            self.on_chat_message(
                datetime.datetime.fromtimestamp(params['time']), params['channel'], params['name'], params['text'], params['role'], params['nameColor'],
                params['isOwner'], params['isStaff'], params['isFollower'], params['isSubscriber'], params['isCommunity'], params['media'], params.get("buffer", False)
            )
        elif method == "chatLog":
            self.on_chat_log(
                datetime.datetime.fromtimestamp(params['timestamp']), params['channel'], params['text'], params.get("buffer", False)
            )

    def on_chat_message(self, timestamp, channel, name, text, role, name_color, is_owner, is_staff, is_follower, is_subscriber, is_community, is_media, is_buffer):
        pass
    
    def on_chat_log(self, timestamp, channel, text, is_buffer):
        pass
   
    #--------------------------------------------------------------------------------------------------------------------------------
    #-- public methods
    #--------------------------------------------------------------------------------------------------------------------------------

    def connect(self):
        num_tries = 0
        while True:
            try:
                num_tries += 1
                self._connect()
            except:
                if num_tries >= 5:
                    raise Exception('could not connect to WebSocket server')
                time.sleep(2)

    def join_channel(self, channel):
        self._send_message(
            'joinChannel',
            {
                'channel': channel.lower(),
                'name': self.username,
                'token': self.auth_token,
                'isAdmin': False
            }
        )

    def send_chat_message(self, channel, text):
        self._send_message(
            'chatMsg',
            {
                'channel': channel.lower(),
                'name': self.username,
                'nameColor': self.name_color,
                'text': text
            }
        )          

    def send_direct_message(self, channel, user, text):
        self._send_message(
            'directMsg',
            {
                'channel': channel.lower(),
                'from': self.username,
                'to': user,
                'nameColor': self.name_color,
                'text': text
            }
        )          

    def kick_user(self, channel, user, timeout=10):
        self._send_message(
            'kickUser',
            {
                'channel': channel.lower(),
                'name': user,
                'token': self.auth_token,
                'timeout': timeout
            }
        )
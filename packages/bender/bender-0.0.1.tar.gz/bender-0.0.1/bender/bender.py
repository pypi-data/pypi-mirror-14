from __future__ import unicode_literals
import re
import json
import requests
from copy import copy
from operator import methodcaller
from redis import StrictRedis


API_URL = "https://api.telegram.org/bot%s/%s"
DEFAULT_HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
BASE_COMMANDS = {'/help': 'help'}


class Bot(object):
    commands = {}

    def __init__(self, token, webhook):
        self.token = token
        self.webhook = webhook
        self.commands.update(BASE_COMMANDS)
        self.redis = StrictRedis(host='localhost',
                                 port=6379,
                                 charset='utf-8',
                                 decode_responses=True,
                                 db=0) # FIXME: default db?
        self.redis_prefix = self.token + ':'

    def _parse_command(self, text):
        command_regexp = r'^(?P<command>/\w+)(?P<mention>@\S+)*\s*(?P<rest>\b.+\n*)*'
        match = re.match(command_regexp, text)
        if match:
            return match.groupdict()
        else:
            return {'command': text, 'rest': None}

    def _get_handler(self, command):
        handler_name = self.commands.get(command['command'], None)
        if handler_name:
            return methodcaller(handler_name, **command)

    def _get_next_step(self):
        next_step = self.redis.get(self.redis_prefix + 'users:' + str(self._from['id']) + ':next_step')
        if next_step:
            return methodcaller(next_step)

    def _end_transaction(self):
        self.redis.delete(self.redis_prefix + 'users:' + str(self._from['id']) + ':next_step')

    def request(self, method, data, headers=DEFAULT_HEADERS):
        url = API_URL % (self.token, method)
        return requests.post(url, data=json.dumps(data), headers=headers)

    def register(self):
        data = {'url': self.webhook+self.token}
        self.request('setWebHook', data)
        return data['url']

    def reply(self, message, *args, **kwargs):
        # FIXME: This is a mess
        # Message classes, maybe?
        data = {'chat_id': self._message['chat']['id'],
                'reply_to_message_id': self._message['message_id'],
                'parse_mode': 'Markdown'}

        sticker = message.get('sticker', None)
        photo = message.get('photo', None)
        caption = message.get('caption', None)
        document = message.get('document', None)
        text = message.get('text', None)
        reply_markup = message.get('reply_markup', None)

        message_queue = []

        if reply_markup:
            data['reply_markup'] = reply_markup

        if text:
            method = 'sendMessage'
            local_data = copy(data)
            local_data['text'] = text
            message_queue.append({'method': method, 'data': local_data})

        if sticker:
            method = 'sendSticker'
            local_data = copy(data)
            del(local_data['reply_to_message_id'])
            local_data['sticker'] = sticker
            message_queue.append({'method': method, 'data': local_data})

        if photo:
            method = 'sendPhoto'
            local_data = copy(data)
            local_data['photo'] = photo
            if caption:
                local_data['caption'] = caption 
            del(local_data['reply_to_message_id'])
            message_queue.append({'method': method, 'data': local_data})

        if document:
            method = 'sendDocument'
            local_data = copy(data)
            del(local_data['reply_to_message_id'])
            local_data['document'] = document
            message_queue.append({'method': method, 'data': local_data})

        for message in message_queue:
            self.request(message['method'], message['data'])

        return True

    def handle_update(self, update):
        self._update = update
        self._from = self._update['message']['from']
        self._message = self._update['message']

        text = self._message.get('text', '')

        command = self._parse_command(text)
        handler = self._get_handler(command)

        if handler:
            handler(self)
        elif not text.startswith('/'):
            next_step = self._get_next_step()

            if next_step:
                next_step(self)

    # bot commands
    def help(self, *args, **kwargs):
        raise NotImplementedError

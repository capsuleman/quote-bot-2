from telebot import TeleBot
from threading import Thread
from functools import wraps


class BotThread(Thread):

    def __init__(self, dao, token, chat_id):
        Thread.__init__(self)
        bot = TeleBot(token)

        def user_required(f):
            @wraps(f)
            def wrapper(*args, **kw):
                msg = args[0]
                if not (msg.chat.id == chat_id or bot.get_chat_member(chat_id, msg.from_user.id).status != 'left'):
                    resp = 'Hi! I\'m the QuoteBot, I store quotes!\n'
                    resp += 'You are not part of my main chan, sorry.'
                    return bot.reply_to(msg, resp)
                return f(*args, **kw)
            return wrapper

        @bot.message_handler(commands=['start'])
        @user_required
        def start(msg):
            chat_id = msg.chat.id
            if msg.chat.type == 'private':
                resp = 'Hi! I\'m the QuoteBot, I store quotes!\n'
                resp += 'Here\'s some command you can use:\n'
                resp += '`/add ||q|| ||a||` to add the quote `q` from `a`\n'
                resp += '`/last n` to get the last n quotes'
            elif msg.chat.id != chat_id:
                resp = 'Hi! Currently the bot is written to handle only one chan, and you are not this one...\n'
                resp += '[Source code](https://github.com/capsuleman/quote-bot-2).'
            else:
                resp = 'Hi! I\'m the QuoteBot, I store quotes! Please send me private message to add quotes.'

            return bot.reply_to(msg, resp, parse_mode='Markdown')

        @bot.message_handler(commands=['add'])
        @user_required
        def add(msg):
            if msg.chat.type != 'private':
                resp = 'Please add quotes in private.'
                return bot.reply_to(msg, resp)
            content = msg.text.split('||')[1]
            author = msg.text.split('||')[3]
            dao.add_quote(content, author)
            resp = 'Quote added!'
            return bot.reply_to(msg, resp, parse_mode='HTML')

        @bot.message_handler(commands=['random'])
        @user_required
        def random(msg):
            chat_id = msg.chat.id
            try:
                n = int(msg.text.split()[1])
            except:
                resp = 'Incorrect argument. Example: `/random 10` to get ten random quotes.'
                return bot.reply_to(msg, resp, parse_mode='Markdown')
            n = max(0, n)
            return self.render_and_send_quotes(msg, dao.get_random_quotes(n))

        @bot.message_handler(commands=['last'])
        @user_required
        def last(msg):
            chat_id = msg.chat.id
            try:
                n = int(msg.text.split()[1])
            except:
                resp = 'Incorrect argument. Example: `/last 10` to get the last ten quotes.'
                return bot.reply_to(msg, resp, parse_mode='Markdown')
            n = max(0, n)
            return self.render_and_send_quotes(msg, dao.get_last_quotes(n))

        @bot.message_handler(commands=['search'])
        @user_required
        def search(msg):
            chat_id = msg.chat.id
            search_key = msg.text[8:]
            if len(search_key) == 0:
                resp = 'No search argument. Example: `/search test` to get the quotes containing `test`.'
                return bot.reply_to(msg, resp, parse_mode='Markdown')
            return self.render_and_send_quotes(msg, dao.search_quotes(search_key))

        self.bot = bot

    def run(self):
        self.bot.polling()

    def render_and_send_quotes(self, msg, quotes):
        if len(quotes) == 0:
            resp = 'No result...'
        else:
            n = len(quotes)
            resp = ''
            for i, quote in enumerate(quotes):
                content = quote.get('content')
                author = quote.get('author')
                resp += '<b>{}</b> \n\n<i>by {}</i>'.format(content, author)
                if i != n-1:
                    resp += '\n\n───────────────\n\n'
        if len(resp) > 4096:
            resp = 'Too many quotes to display...'
        return self.bot.reply_to(msg, resp, parse_mode='HTML')

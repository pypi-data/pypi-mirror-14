"""
critbot.plugins.slack
https://github.com/denis-ryzhkov/critbot

@author Denis Ryzhkov <denisr@denisr.com>
"""

### plugin

class plugin(object):

    def __init__(self,
        token, # Get it from https://my.slack.com/services/new/bot
        channel='#general', # '@private' or '#channel'
        users='', # '@user1 @user2 @userN'
        icon_emoji=':fire:',
        bot_name='CRIT-bot',
        seconds_per_notification=60,
    ):
        self.token = token
        self.channel = channel
        self.users = users
        self.icon_emoji = icon_emoji
        self.bot_name = bot_name
        self.seconds_per_notification = seconds_per_notification
        self.last_notification_timestamp = 0

    def send(self, subject, text):

        from requests import post
            # This import is postponed intentionally:
            # it may be slow because of "pyopenssl",
            # while small scripts may neither produce a crit, nor need this import.
            # Once imported, it is cached in "sys.modules", so multiple crits have no overhead.

        text = '```{}```'.format(text.replace('```', '???'))
        text = '{} {}'.format(self.users, text).lstrip()
        text = '{} {}'.format(subject, text).lstrip()

        data = dict(
            token=self.token,
            channel=self.channel,
            icon_emoji=self.icon_emoji,
            username=self.bot_name,
            parse='full',
            text=text,
        )

        post('https://slack.com/api/chat.postMessage', data=data)

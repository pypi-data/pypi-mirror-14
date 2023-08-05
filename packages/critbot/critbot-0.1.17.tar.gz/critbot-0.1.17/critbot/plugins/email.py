"""
critbot.plugins.email
https://github.com/denis-ryzhkov/critbot

@author Denis Ryzhkov <denisr@denisr.com>
"""

### import

from send_email_message import send_email_message

### plugin

class plugin(object):

    def __init__(self,
        to, # 'Name1 <user1@example.com>, Name2 <user2@example.com>'
        user, # 'critbot@example.com'
        password, # 'pa$$word'
        from_name='CRIT-bot',
        # Default settings are for GMail.
        # "Yandex" comments are for https://domain.yandex.com/
        host='smtp.gmail.com', # Yandex: 'smtp.yandex.com'
        port=587, # Yandex: 465
        ssl=False, # Yandex: True
        tls=True, # Yandex: False
        login_plain=False, # Some servers are OK with TLS, but require "LOGIN PLAIN" auth inside encrypted session.
        debug=False, # Enables debug output.
        seconds_per_notification=60,
    ):
        self.email_config = dict(to=to, user=user, password=password, from_name=from_name,
            host=host, port=port, ssl=ssl, tls=tls, login_plain=login_plain, debug=debug,
        )
        self.seconds_per_notification = seconds_per_notification
        self.last_notification_timestamp = 0

    def send(self, subject, text):
        send_email_message(subject=subject, text=text, **self.email_config)

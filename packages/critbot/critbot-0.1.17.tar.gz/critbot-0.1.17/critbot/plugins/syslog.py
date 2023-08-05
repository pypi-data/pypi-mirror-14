"""
critbot.plugins.syslog
https://github.com/denis-ryzhkov/critbot

@author Denis Ryzhkov <denisr@denisr.com>
"""

### import

import logging
import logging.handlers
import re
import sys

### plugin

class plugin(object):

    def __init__(self,
        logger_name='critbot',
        logger_level=logging.CRITICAL,
        seconds_per_notification=0, # Log all crits.
        **handler_kwargs # https://docs.python.org/2/library/logging.handlers.html#logging.handlers.SysLogHandler
        # If "address" is not specified, it will guess an efficient local address depending on OS.
    ):
        if 'address' not in handler_kwargs:
            handler_kwargs['address'] = (
                '/dev/log' if sys.platform.startswith('linux') else
                '/var/run/syslog' if sys.platform.startswith('darwin') else # Mac OS X
                ('localhost', 514) # Windows, etc.
            )

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)
        self.handler = logging.handlers.SysLogHandler(**handler_kwargs)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False # It has its own handler, so should avoid double logging.
        self.seconds_per_notification = seconds_per_notification
        self.last_notification_timestamp = 0
        self.new_line_from = re.compile('[\r\n]+')
        self.new_line_to = ' | ' # Better than "#012" in syslog.

    def send(self, subject, text):
        text = '{} {}'.format(subject, text).lstrip()
        text = self.new_line_from.sub(self.new_line_to, text)
        self.logger.critical(text)

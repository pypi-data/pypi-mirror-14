"""
"critbot" lib.
https://github.com/denis-ryzhkov/critbot

@author Denis Ryzhkov <denisr@denisr.com>
"""

### import

from adict import adict
import time
from traceback import format_exc
import sys

### crit_defaults

crit_defaults = adict(
    subject='CRIT', # '{service_name} {host}:{port} CRIT'
    plugins=[], # [critbot.plugins.syslog.plugin(), ...]
    crit_in_crit=sys.stderr.write, # logging.getLogger('critbot').critical - if you enabled "syslog" plugin, else your_logger.critical

    mc=adict( # Memcached to stop spam from multiple processes.
        enabled=False,
        servers=['127.0.0.1'], # http://sendapatch.se/projects/pylibmc/reference.html#pylibmc.Client
        client_config=adict(binary=True, behaviors=dict(tcp_nodelay=True, distribution='consistent')),
        pool_size=10,
        pool=None, # Is initialized on first crit from updated crit_defaults and to avoid useless slowdown in small scripts.
    ),
)

### utf8

def utf8(value):
    return (
        value.encode('utf8') if isinstance(value, unicode) else
        value if isinstance(value, str) else
        str(value)
    )

### crit

def crit(only='', also='', subject='', plugins=None, spam=False):
    """
    Sends critical error.

    @param str only - The only details of crit, don't include traceback.
    @param str also - Additional details of crit to add to traceback.
    @param str subject - Subject of this crit instead of "crit_defaults.subject".
    @param list plugins - Plugins to send this crit to instead of "crit_defaults.plugins".
    @param bool spam - Ignore "plugin.seconds_per_notification", do spam on each crit.
    @return NoneType
    """

    try:

        ### text

        text = utf8(only) or '{} {}'.format(utf8(also), format_exc()).lstrip()

        ### mc_pool

        mc_pool = None
        if crit_defaults.mc.enabled:
            mc_pool = crit_defaults.mc.pool
            if not mc_pool:
                try:
                    import pylibmc
                    mc_pool = crit_defaults.mc.pool = pylibmc.ClientPool(
                        pylibmc.Client(crit_defaults.mc.servers, **crit_defaults.mc.client_config),
                        crit_defaults.mc.pool_size,
                    )
                except Exception:
                    crit_defaults.crit_in_crit(format_exc())

        ### plugins, seconds_per_notification

        now = time.time()
        for plugin in plugins or crit_defaults.plugins:

            if not spam:
                if mc_pool and plugin.seconds_per_notification: # Don't bother Memcached for "syslog" and other "seconds_per_notification=0" plugins.
                    try:
                        with mc_pool.reserve(block=True) as mc:
                            if not mc.add(plugin.__module__ + '.antispam', '1', time=plugin.seconds_per_notification):
                                continue # E.g. key "critbot.plugins.slack.antispam" still exists.
                    except Exception:
                        crit_defaults.crit_in_crit(format_exc())

                if now - plugin.last_notification_timestamp < plugin.seconds_per_notification:
                    continue

            plugin.last_notification_timestamp = now

            ### send

            try:
                plugin.send(subject or crit_defaults.subject, text)

            ### crit_in_crit

            except Exception:
                crit_defaults.crit_in_crit(format_exc())

    except Exception:
        crit_defaults.crit_in_crit(format_exc())

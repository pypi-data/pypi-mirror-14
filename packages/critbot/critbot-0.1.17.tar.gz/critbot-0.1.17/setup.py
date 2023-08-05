from distutils.core import setup

setup(
    name='critbot',
    version='0.1.17',
    description='Sending critical errors to syslog, slack, email, {your_plugin}.',
    long_description='''
Install::

    pip install critbot

Add to "config.py" file::

    import critbot.plugins.syslog
    import critbot.plugins.slack
    import critbot.plugins.email
    from critbot import crit_defaults
    import logging

    crit_defaults.subject = 'MyService host:port CRIT'

    crit_defaults.plugins = [
        critbot.plugins.syslog.plugin(),
        critbot.plugins.slack.plugin(
            token='Get it from https://my.slack.com/services/new/bot',
            channel='#general', # '@private' or '#channel'
            users='', # '@user1 @user2 @userN'
        ),
        critbot.plugins.email.plugin(
            to='Name1 <user1@example.com>, Name2 <user2@example.com>',
            user='critbot@example.com', # Add more config if not GMail.
            password='pa$$word',
        ),
    ]

    crit_defaults.crit_in_crit = logging.getLogger('critbot').critical

Check other config options and their defaults, e.g. "seconds_per_notification=60" and "spam=False":

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/core.py#L23 - "crit_defaults"

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/core.py#L38 - "crit"

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/syslog.py#L17

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/slack.py#L14

* https://github.com/denis-ryzhkov/critbot/blob/master/critbot/plugins/email.py#L14

Use "crit" in other files of your project::

    from my_project import config
    from critbot import crit

    try:
        1/0
    except Exception:
        crit()
        # More processing if needed.

    try:
        1/0
    except Exception:
        crit(also='test2')

    if True:
        crit('test3')

If you are using http://supervisord.org/  
then you can monitor stderr, EXITED and FATAL states with::

    [eventlistener:critvisor]
    command=critvisor /path/to/config.py
    events=PROCESS_LOG_STDERR,PROCESS_STATE_EXITED,PROCESS_STATE_FATAL

    [program:my_program]
    stderr_events_enabled=true

    Optional "crit_defaults.skip_stderrs" list allows to avoid some "safe" crits.
    Optional "crit_defaults.max_stderr_crit_length" allows to save e.g. Slack from being broken.

If you want to convert stderr of your small scripts to crits::

    stdcrit /path/to/config.py /path/to/script.py arg...

To stop spam from multiple processes::

    apt-get install libmemcached-dev zlib1g-dev
    pip install pylibmc
    crit_defaults.mc.enabled = True

    And either "apt-get install memcached"
    or update "crit_defaults.mc.servers" list.

Please fork https://github.com/denis-ryzhkov/critbot
and create pull requests with new plugins inside.

''',
    url='https://github.com/denis-ryzhkov/critbot',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'critbot',
        'critbot.plugins',
    ],
    scripts=[
        'scripts/critvisor',
        'scripts/stdcrit',
    ],
    install_requires=[
        'adict',
        'requests',
        'send_email_message',
    ],
)

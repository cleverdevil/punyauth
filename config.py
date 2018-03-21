# Server Specific Configurations
server = {'port': '8081', 'host': '127.0.0.1'}

# Pecan Application Configurations
app = {
    'root': 'punyauth.controllers.root.RootController',
    'modules': ['punyauth'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/punyauth/templates',
    'debug': True,
    'force_canonical': False,
}

token = {'algorithm': 'HS256', 'secret': '3598ECD3-6FBE-443A-B8E3-8D5E548F0608'}

passwords = {'path': '%(confdir)s/etc/passwords.json', 'salt': '82E4D540'}

logging = {
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'punyauth': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
        'pecan': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True,
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': (
                '%(asctime)s %(levelname)-5.5s [%(name)s]'
                '[%(threadName)s] %(message)s'
            )
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': (
                '%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                '[%(threadName)s] %(message)s'
            ),
            '__force_dict__': True,
        },
    },
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf

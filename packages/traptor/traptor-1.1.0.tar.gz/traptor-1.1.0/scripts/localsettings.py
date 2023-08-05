mysql_settings = {
    'HOST': 'memex-db.istresearch.com',
    'PORT': 3306,
    'USER': 'memex',
    'PASSWD': 'pDYKV39gySsHcPhzpjTbgkM6',
    'DB': 'memex_cooper_prod'
}

# redis_settings = {
#     'HOST': 'memex-services.istresearch.com',
#     'PORT': 6379,
#     'DB': 1
# }

# Local Overrides
# ~~~~~~~~~~~~~~~

try:
    from localsettings import *
except ImportError:
    pass

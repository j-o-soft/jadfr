try:
    from settings_local import MyConf
except ImportError:
    from feedreader.conf.base import Dev as MyConf

try:
    from settings_local import MyTestConf
except ImportError:
    from feedreader.conf.base import Test as MyTestConf

try:
    from settings_local import MyConf
except ImportError:
    from feedreader.conf.base import Dev

    class MyConf(Dev):
        pass

try:
    from settings_local import MyTestConf
except ImportError:
    from feedreader.conf.base import Dev as MyTestConf
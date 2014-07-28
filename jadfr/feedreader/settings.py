from conf.my_conf import MyConf
from conf.base import Production

if not issubclass(MyConf, Production):
    from conf.my_conf import MyTestConf

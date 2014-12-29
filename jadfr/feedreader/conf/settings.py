__author__ = 'j_schn14'
try:
    from my_conf import MyConf
except ImportError:
    pass

try:
    from my_conf import MyTestConf
except ImportError:
    from base import Test as MyTestConf




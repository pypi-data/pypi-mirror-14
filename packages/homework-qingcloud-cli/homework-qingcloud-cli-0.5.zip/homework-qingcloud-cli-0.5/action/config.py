import os
import yaml


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


@singleton
class Config(object):
    access_key_id = ''
    secret_access_key = ''
    zone = ''
    base_url = 'https://api.qingcloud.com/iaas/?'
    def __init__(self):
        require_params = [
                "qy_access_key_id",
                "qy_secret_access_key",
                "zone",
                ]

        config_path = os.path.expanduser('~') + '/.qingcloud/config.yaml'

        if not os.path.isfile(config_path):
            print("config file [%s] not exists" % config_path)
            return None

        with open(config_path, "r") as fd:
            conf = yaml.load(fd)
            if conf is None:
                print("config file [%s] format error" % config_path)
                return None
            for param in require_params:
                if param not in conf:
                    print("[%s] should be specified in conf_file" % param)
                    return None
        self.access_key_id = conf.get('qy_access_key_id')
        self.secret_access_key = conf.get('qy_secret_access_key')
        self.zone = conf.get('zone')
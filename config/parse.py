import os
import yaml
from yaml import Loader


def get_config():
    cfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml')

    if not os.path.exists(cfile):
        raise "文件路径不存在"

    with open(cfile, 'r') as fp:
        conf = yaml.load(fp, Loader)

    for vals in conf.values():
        for k, v in vals.items():
            os.environ.setdefault(k, str(v))

    return conf



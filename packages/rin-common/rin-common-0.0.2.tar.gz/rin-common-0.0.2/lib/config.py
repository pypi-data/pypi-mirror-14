import sys,os,yaml

class Config(object):
    DEFAULT_PATH = '/usr/local/etc/rin.yml'

    @classmethod
    def load(self, path = DEFAULT_PATH):
        if os.path.isfile(path):
          with open(path, 'r') as f:
            return yaml.load(f)

import yaml
import os.path
import collections


class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

    def secret(self, node):
        filename = os.path.join(self._root, "secrets.yaml")
        with open(filename, 'r') as f:
            secrets = yaml.load(f, Loader)
            return secrets[self.construct_scalar(node)]


Loader.add_constructor('!include', Loader.include)
Loader.add_constructor('!secret', Loader.secret)


class Settings(collections.MutableMapping):
    __instance = None

    def __getitem__(self, k):
        return self.store[self.__keytransform__(k)]

    def __keytransform__(self, key):
        return key

    def __len__(self) -> int:
        return len(self.store)

    def __iter__(self):
        return iter(self.store)

    def __delitem__(self, v):
        pass

    def __setitem__(self, k, v):
        pass

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception('This class is a singleton')
        else:
            script_path = os.path.realpath(__file__)
            script_folder = os.path.dirname(os.path.dirname(script_path))

            with open('{}/config/settings.yaml'.format(script_folder), 'r') as config:
                self.store = yaml.load(config, Loader)

            Settings.__instance = self

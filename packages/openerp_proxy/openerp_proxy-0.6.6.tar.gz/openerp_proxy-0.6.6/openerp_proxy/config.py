from .utils import AttrDict
__all__ = ('config',)


class Config(dict):
    def get(self, opt, default):
        if opt not in self:
            self[opt] = default
        return self[opt]

config = Config()

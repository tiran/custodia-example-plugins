from __future__ import absolute_import

from custodia.plugin import CSStore, CSStoreError
from custodia.plugin import PluginOption, REQUIRED


class ExampleStore(CSStore):
    backing_store = PluginOption(str, REQUIRED, None)

    def __init__(self, config, section):
        super(ExampleStore, self).__init__(config, section)
        self.store_name = self.backing_store
        self.store = None

    def get(self, key):
        value = self.store.get(key)
        if value is None:
            return None
        if value != 'example':
            raise CSStoreError('Invalid value')
        return value

    def set(self, key, value, replace=False):
        if value != 'example':
            raise CSStoreError('Invalid value')
        return self.store.set(key, value, replace)

    def span(self, key):
        return self.store.span(key)

    def list(self, keyfilter=''):
        return self.store.list(keyfilter)

    def cut(self, key):
        return self.store.cut(key)

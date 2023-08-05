import os
import pickle

class PersistentData(object):
    def __init__(self, fpath, fname, defaults={}):
        if not fpath:
            fpath=os.path.dirname(os.path.realpath(__file__))
        self._fpath=os.path.expanduser(fpath)
        self._fname=fname
        self._data={}
        self._updated=False
        self.load(defaults)

    def fpath(self):
        if not os.path.exists(self._fpath):
            os.makedirs(self._fpath)
        return os.path.join(self._fpath, self._fname)

    def data(self):
        return self._data

    def importData(self, data):
        try:
            for key in data.keys():
                self.set(key, data[key])
        except:
            pass

    def importDefaultData(self, data):
        try:
            for key in data.keys():
                try:
                    if not self.has(key):
                        self.set(key, data[key])
                except:
                    pass
        except:
            pass

    def load(self, defaults={}):
        try:
            with open(self.fpath(), 'rb') as f:
                self._data=pickle.load(f)
                self.importDefaultData(defaults)
        except:
            self._data=defaults
        return self._data

    def save(self):
        try:
            if self._updated:
                with open(self.fpath(), 'wb') as f:
                    pickle.dump(self._data, f)
                    self._updated=False
            return True
        except:
            pass

    def set(self, key, value):
        try:
            if self.get(key)!=value:
                self._data[key]=value
                self._updated=True
                return True
        except:
            pass

    def has(self, key):
        try:
            self._data[key]
            return True
        except:
            pass

    def get(self, key, default=None):
        try:
            return self._data[key]
        except:
            return default

    def __getitem__(self, key):
        return self.get(key)


if __name__ == "__main__":
    pass


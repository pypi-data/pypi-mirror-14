import pickle
import hashlib


class CacheManager(object):
    def __init__(self):
        self.cache_db_file = ".cache.db"
        self.cache_db = dict()
        self.transient_cache_db = dict()

    def load_cache(self, cache_db_file=None):
        if cache_db_file:
            self.cache_db_file = cache_db_file
        try:
            pickled = pickle.load(open(self.cache_db_file))
            self.cache_db = dict(pickled)
        except IOError:
            self.cache_db = dict()

    def register(self, file_path):
        checksum = hashlib.md5(open(file_path).read()).hexdigest()
        if self.cache_db.get(file_path, None) != checksum:
            self.cache_db[file_path] = checksum
            self.transient_cache_db[file_path] = True
        else:
            self.transient_cache_db[file_path] = False

    def is_file_changed(self, file_path):
        if file_path in self.transient_cache_db:
            return self.transient_cache_db[file_path]
        else:
            self.register(file_path)
            return True

    def close(self):
        pickle.dump(
            self.cache_db.items(),
            open(self.cache_db_file, "w"))


cache_manager = CacheManager()
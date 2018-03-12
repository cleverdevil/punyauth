import time
import threading


class TTLCache:
    def __init__(self, ttl=120):
        self.cache = {}
        self.ttl = ttl
        self.lock = threading.Lock()

    def set(self, key, payload):
        with self.lock:

            self.cache[key] = payload

            def expire():
                time.sleep(self.ttl)
                with self.lock:
                    del self.cache[key]

            threading.Thread(target=expire).start()

    def get(self, key):
        with self.lock:
            return self.cache.get(key)


cache = TTLCache(ttl=600000)


def set(payload):
    key = '%s%s%s' % (
        payload['code'],
        payload['redirect_uri'],
        payload['client_id']
    )
    print('Setting key: "%s"' % key)
    cache.set(key, payload)


def get(payload):
    key = '%s%s%s' % (
        payload['code'],
        payload['redirect_uri'],
        payload['client_id']
    )
    print('Searching key: "%s"' % key)
    return cache.get(key)

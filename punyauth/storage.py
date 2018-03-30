from pecan import conf

import json
import time
import threading
import boto3
import io


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


class S3Cache:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def set(self, key, payload):
        payload = json.dumps(payload).encode('utf-8')
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=payload)

    def get(self, key):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        except:
            return None

        else:
            return json.loads(response['Body'].read().decode('utf-8'))


if conf.token.get('s3bucket'):
    cache = S3Cache(conf.token.get('s3bucket'))
else:
    cache = TTLCache()


def set(payload):
    key = '%s%s%s' % (payload['code'], payload['redirect_uri'], payload['client_id'])
    cache.set(key, payload)


def get(payload):
    key = '%s%s%s' % (payload['code'], payload['redirect_uri'], payload['client_id'])
    return cache.get(key)

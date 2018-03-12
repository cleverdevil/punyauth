from pecan import conf

import tinydb
import threading


db = tinydb.TinyDB(conf.db.path, create_dirs=True)
lock = threading.Lock()

def store(json, table='_default'):
    with lock:
        doc_id = db.table(table).insert(json)
        return doc_id


def get(doc_id, table='_default'):
    with lock:
        return db.table(table).get(doc_id=doc_id)


def find(table='_default', **kw):
    Query = tinydb.Query()
    conditions = [
        getattr(Query, key) == val
        for key, val in kw.items()
    ]
    condition = conditions.pop()
    for c in conditions:
        condition = condition & c
    return db.table(table).search(condition)


def delete(doc_id, table='_default'):
    return db.table(table).remove(doc_ids=[doc_id])

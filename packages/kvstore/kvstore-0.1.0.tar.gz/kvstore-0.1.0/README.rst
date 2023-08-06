Python KeyValue Store abstraction API
=====================================

Purpose
-------
The objective of this module is to provide a common API to different KeyValue stores
like consul, etcd or zookeeper.

Usage examples
--------------
Basic usage examples::

    import kvstore
    kv = kvstore.Client()
    kv.set(key, value)
    kv.get(key)
    kv.recurse(key)
    kv.delete(key)
    kv.delete(key, recursive=True)
    kv.index(key, recursive=True)
    kv.get(key, wait=True, index=index, wait='10m')
    kv.recurse(key, wait=True, index=index, wait='10m')

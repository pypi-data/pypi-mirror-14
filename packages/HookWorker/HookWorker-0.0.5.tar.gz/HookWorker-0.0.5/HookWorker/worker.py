#!/usr/bin/env python3
import os
from rq import Queue, Connection, Worker
import redis

# Preload libraries
import HookTest.test

def worker(redis_url="localhost:6379"):
    """ Run a work for python-rq

    :param redis_url: Redis URI (redis://{redis_url})
    :type redis_url: str

    """
    redis_url = "redis://{0}".format(redis_url)
    conn = redis.from_url(redis_url)

    with Connection(conn):
        qs = [Queue("hook")]

        w = Worker(qs)
        w.work()


if __name__ == "__main__":
    worker()

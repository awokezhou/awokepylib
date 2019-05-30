from __future__ import absolute_import

import time


def time_consumption(function):
    def wrapper(*args, **kwargs):
        name = function.__name__
        t0 = time.time()
        ret = function(*args, **kwargs)
        elapsed = time.time() - t0
        print("--> {}() time consumption {}".format(name, time_second_to_slot(elapsed)))
        return ret
    return wrapper

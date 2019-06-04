from __future__ import absolute_import

from concurrent import futures
from progressbar import ProgressBar

def concurrent_process_thread_poll(do_iter, fn_one, n_workers, data, pb=True, pb_desc=None):
    if not pb_desc:
        description = 'Concurrent Process({} workers)'.format(n_workers)
    else:
        description = '{}({} workers)'.format(pb_desc, n_workers)

    with futures.ThreadPoolExecutor(n_workers) as executor:
        to_do = []
        for item in sorted(do_iter):
            argvs = (item, data)
            future = executor.submit(fn_one, *argvs)
            to_do.append(future)

        results = []
        done_iter = futures.as_completed(to_do)
        if pb == True:
            done_iter = ProgressBar(done_iter, progressbar_type='concurrent',
                desc_prefix=description, total=len(do_iter))
            for future in done_iter.get_iter():
                res = future.result()
                results.append(res)
        else:
            for future in done_iter:
                res = future.result()
                results.append(res)
    return len(results)

def test_one(item, data):
    data.append(item)

def test():
    list = range(10)
    data = []
    concurrent_process_thread_poll(list,
                                   test_one,
                                   2,
                                   data,
                                   True,
                                   'current test')
    print data

import sys
sys.path.append("..")
from concurrent import futures
from lib.progressbar import ProgressBar

def concurrent_process_thread_poll(do_iter, fn_one, n_workers, pb, pb_desc, data):
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

def test_one(item):
    item = 2

def test():
    list = range(100000)
    concurrent_process_thread_poll(list,
                                   test_one,
                                   5,
                                   'CC test')

from __future__ import absolute_import

import os
import csv
import time
import linecache
from lib import schedule
from lib.progressbar import ProgressBar


class Batcher(object):

    def __init__(self, filename, batch_size=2000, offset=0, end=None):
        self.filename = filename
        try:
            self._n_lines = lines(self.filename)
        except Exception as e:
            print e

        if batch_size > self._n_lines:
            self._size = self._n_lines
            self._n_batchs = 1
            print 'batch_size too big, adjust to file lines {}'.format(self._n_lines)
        else:
            self._size = batch_size
            self._n_batchs = (self._n_lines/self._size) + 1
        self._offset = offset
        self._end = end
        self.getlines = linecache.getlines
        self.clearcache = linecache.clearcache

    def _batch(self):
        if self._end and self._offset >= self._end:
            return None
        offset = self._offset
        size = self._size
        end = offset+size
        batch = self.getlines(self.filename)[offset:end]
        self._offset += size
        return batch

    def __iter__(self):
        while True:
            batch = self._batch()
            if not batch:
                break
            yield batch

    def __del__(self):
        self.clearcache()

def lines(filename):
    line_nr = 0
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line_nr += 1
    return line_nr

def batch_concurrent_process(filename, batch_size, n_workers):
    list = []
    filelines = file_lines(filename)
    print 'filelines {}'.format(filelines)
    def _once(item, list):
        list.append(item[0])

    class Batch(object):
        def __init__(self, filename, batch_size):
            self.filename = filename
            self.batch_size = batch_size
            self._offset = 0
            self.getlines = linecache.getlines

        def _batch(self):
            offset = self._offset
            size = self.batch_size
            end = offset+size
            batch = self.getlines(self.filename)[offset:end]
            self._offset += size
            return batch

        def __iter__(self):
            while True:
                batch = self._batch()
                if not batch:
                    break
                yield batch

    count = 0
    n_batchs = (filelines/batch_size)+1
    print 'n_batchs {}'.format(n_batchs)
    #with open(filename, 'r') as f:
    bar = ProgressBar(Batch(filename, batch_size),
                      progressbar_type='concurrent',
                      total=n_batchs,
                      desc_prefix='batch concurrent test')
    for batch in bar.get_iter():
        count += 1
        if n_workers >= 2:
            schedule.concurrent_process_thread_poll(batch, _once, 5, False, None, list)
        else:
            for item in batch:
                _once(item, list)
    print count
    print len(list)

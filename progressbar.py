from __future__ import absolute_import

import time
import tqdm
import copy


class ProgressBar(object):

    """A custom progress bar class encapsulating tqdm.

    -- progressbar_type --
        iteration: input do_iter is a list, know len
        concurrent: input do_iter is a iterator, dont know len,
    """

    DEFAULT_CONFIG = {
        'progressbar_type':'iteration',     # iteration/stage/concurrent
        'desc_prefix':'Processing',
        'total':0,
    }

    def __init__(self, do_iter, **configs):
        self.config = copy.copy(self.DEFAULT_CONFIG)
        for key in self.config:
            if key in configs:
                self.config[key] = configs.pop(key)

        if self.config['progressbar_type'] == 'iteration':
            self._iter = tqdm.tqdm(do_iter, desc=self.config['desc_prefix'])
        elif self.config['progressbar_type'] == 'stage':
            self._iter = tqdm.tqdm(desc=self.config['desc_prefix'],
                                   total=self.config['total'])
        elif self.config['progressbar_type'] == 'concurrent':
            self._iter = tqdm.tqdm(do_iter, desc=self.config['desc_prefix'],
                                   total=self.config['total'])
    def get_iter(self):
        return self._iter

    def update(self, **postfix):
        self._iter.set_postfix(postfix)
        self._iter.update(1)

    def close(self):
        self._iter.close()

class StageProgressBar(object):

    def __init__(self, header, complete_str):
        self.header = header
        self.complete_str = complete_str
        self.stage_name = ""
        self.stage_percent = 0
        self.stage_percent_old = 0
        self.stage_iter_max = 0
        self.percent = 0
        self.refresh()

    def new_stage(self, stage_name, stage_percent, stage_iter_max):
        self.stage_name = stage_name
        self.stage_percent_old += self.stage_percent
        self.stage_percent = stage_percent
        self.stage_iter_max = stage_iter_max

    def stage_update(self):
        self.percent += self.stage_percent
        self.refresh()

    def refresh(self):
        header = self.header
        percent = self.percent
        process_str = '[' + '='*percent + ' '*(100-percent) + ']'
        percent_str = '%s%%'%(percent)
        stage_str = "(%s)"%(self.stage_name)
        if system_is_linux() == True:
            sys.stdout.write('\r'+header+" "+stage_str+" "+process_str+" "+percent_str+" ")
        else:
            sys.stdout.write('\b'+header+" "+stage_str+" "+process_str+" "+percent_str+" ")
        sys.stdout.flush()

    def update(self, k):
        self.percent = (k+1)*self.stage_percent/self.stage_iter_max + self.stage_percent_old
        self.refresh()

    def complete(self):
        print(" {}".format(self.complete_str))

class IterProgressBar(object):

    def __init__(self, header, complete, max):
        self.header = header
        self.complete = complete
        self.percent = 0
        self.iter_max = max
        self.refresh('')

    def refresh(self, desc):
        header = self.header
        percent = self.percent
        process_str = '[' + '='*percent + ' '*(100-percent) + ']'
        percent_str = '%s%%'%(percent)
        dump = header + ' ' + process_str + ' ' + percent_str + ' ' + desc
        if system_is_linux() == True:
            sys.stdout.write('\r' + dump)
        else:
            sys.stdout.write('\b'+ dump)
        sys.stdout.flush()

    def update(self, k, desc=''):
        self.percent = (k+1)*100/self.iter_max
        self.refresh(desc)
        if self.percent == 100:
            print(" {}".format(self.complete))

def IterProgressBarTest():
    list = [1,2,3,4,5]
    bar = ProgressBar(list)
    for item in bar.get_iter():
        time.sleep(1)

def stage01():
    a = 1
    time.sleep(5)

def stage02():
    a = 2
    time.sleep(5)

def stage03():
    a = 3
    time.sleep(5)

def StageProgressBarTest():
    bar = ProgressBar(do_iter=None, progressbar_type='stage', total=3)
    stage01()
    bar.update(stage1='finished')
    stage02()
    bar.update(stage2='finished')
    stage03()
    bar.update(stage3='finished')
    bar.close()

import os
import time

import numpy as np


class OnesArrayMaker(object):
    def __init__(self, shape, dtype):
        self.shape = shape
        self.dtype = dtype

    def make_array(self):
        return np.ones(self.shape, self.dtype)


class RandomArrayMaker(object):
    def __init__(self, shape, dtype, seed=None):
        self.shape = shape
        self.dtype = dtype
        self.seed = seed
        self.random_state = None

    def make_array(self):
        pid = os.getpid()
        if self.random_state is None:
            if self.seed is None:
                self.seed = pid
            # print('Creating RandomState({0}) in child process {1}'
            #       .format(self.seed, pid))
            self.random_state = np.random.RandomState(seed=self.seed)
        # print('Making array in child process {}'.format(pid))
        array = self.random_state.rand(*self.shape).astype(self.dtype)
        return array


class SlowArrayMaker(object):
    def __init__(self, shape, dtype, time_lag_in_seconds):
        self.shape = shape
        self.dtype = dtype
        self.time_lag_in_seconds = time_lag_in_seconds

    def make_array(self):
        time.sleep(self.time_lag_in_seconds)
        return np.zeros(self.shape, self.dtype)

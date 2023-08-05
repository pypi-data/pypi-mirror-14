import multiprocessing
import os
import time
from operator import mul

import numpy as np


def refresh_array():
    start = time.time()
    array = make_array()
    with shared_array.get_lock():
        shared_array[:] = array.flatten()
    end = time.time()
    # print('Seconds to refresh array and store in shared memory: {}'.format(end - start))
    return


class AsynchronouslyRefreshableArray(object):
    def __init__(self, array_maker):
        self.array_maker = array_maker
        ctype_of_array_maker = self._get_ctype_of_array_maker(array_maker)
        size_of_array_maker = reduce(mul, array_maker.shape)
        self.mp_array = multiprocessing.Array(
            ctype_of_array_maker,
            size_of_array_maker,
            lock=True)
        self.pool = multiprocessing.Pool(
            processes=1,
            initializer=self._initialize_worker,
            maxtasksperchild=50
        )
        self.last_time_refreshed = None
        return

    @staticmethod
    def _get_ctype_of_array_maker(array_maker):
        # # potential refactor:
        # sample_array = array_maker.make_array()
        # array_maker_type = np.ctypeslib.ndpointer(
        #     dtype=sample_array.dtype,
        #     ndim=sample_array.ndim,
        #     shape=sample_array.shape,
        #     flags=sample_array.flags
        # )
        # ctype_of_array_maker = type(
        #     np.ctypeslib.as_ctypes(array_maker_type._dtype_.type(0)[()]))
        sample_number = 0
        ctype_of_array_maker = type(
            np.ctypeslib.as_ctypes(array_maker.dtype(sample_number)))
        return ctype_of_array_maker

    def _initialize_worker(self):
        # print('Initializing child process {}'.format(os.getpid()))
        global shared_array
        shared_array = self.mp_array
        global make_array
        make_array = self.array_maker.make_array
        return

    def refresh(self, callback=None):
        def callback_for_pool(pool_func_return_value):
            if self.last_time_refreshed:
                # print('Seconds since last refresh: {}'
                #       .format(time.time() - self.last_time_refreshed))
                pass
            self.last_time_refreshed = time.time()
            if callback:
                return callback(self)
            else:
                return pool_func_return_value

        async_result = self.pool.apply_async(func=refresh_array,
                                             callback=callback_for_pool)
        return async_result

    @property
    def value(self):
        with self.mp_array.get_lock():
            numpy_array = np.frombuffer(
                buffer=self.mp_array.get_obj(),
                dtype=self.array_maker.dtype).reshape(self.array_maker.shape)
        return numpy_array

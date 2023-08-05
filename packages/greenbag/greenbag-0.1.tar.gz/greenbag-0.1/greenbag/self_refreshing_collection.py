import time


class SelfRefreshingCollection(object):
    def __init__(self, initial_size, refreshable_element_factory):
        self.collection = []
        self.stale_elements = []
        for _ in range(initial_size):
            new_element = refreshable_element_factory.make_refreshable_element()
            new_element.refresh(self._add_element)

    def _add_element(self, element):
        self.collection.append(element)

    def _start_refreshing_stale_elements(self):
        for stale_element in self.stale_elements:
            stale_element.refresh(callback=self._add_element)
        self.stale_elements = []

    def _pop_element(self):
        while len(self.collection) == 0:
            time.sleep(.001)
            continue
        return self.collection.pop(0)

    def __iter__(self):
        return self

    def __next__(self):
        self._start_refreshing_stale_elements()
        element = self._pop_element()
        self.stale_elements.append(element)
        return element.value

    def next(self):
        return self.__next__()

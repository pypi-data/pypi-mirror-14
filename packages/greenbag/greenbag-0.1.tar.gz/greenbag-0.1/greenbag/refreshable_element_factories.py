class SimpleRefreshableElementFactory():
    def __init__(self, RefreshableElement):
        self.RefreshableElement = RefreshableElement

    def make_refreshable_element(self):
        return self.RefreshableElement()


class RefreshableArrayFactory():
    def __init__(self, RefreshableArray, array_maker):
        self.RefreshableArray = RefreshableArray
        self.array_maker = array_maker

    def make_refreshable_element(self):
        return self.RefreshableArray(self.array_maker)

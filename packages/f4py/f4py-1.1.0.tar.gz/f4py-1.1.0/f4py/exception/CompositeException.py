class CompositeException(Exception):
    def __init__(self, e1, e2):
        super().__init__(e1)
        self.__cause__ = e2

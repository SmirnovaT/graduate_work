class EmptyIndexError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = "Index is empty"

    def __str__(self):
        return f'{self.index}: {self.message}'

class ObjectNotExistException(Exception):

    def __init__(self, message="Object does not exist in base"):
        self.message = message
        super().__init__(self.message)

class Resource:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

    def create(self):
        raise NotImplementedError

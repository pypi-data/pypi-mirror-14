class BaseDefinition(object):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return '<{}>'.format(self.identifier)

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

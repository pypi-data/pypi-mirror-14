class DefinitionConflictError(Exception):
    pass


class UndefinedTypeError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class ExecutionResult(object):
    def __init__(self, message, diff=None, success=True):
        self.message = message
        self.diff = diff
        self.success = success


class Dependency(object):
    def __init__(self, type, name, parameters):
        self.type = type
        self.name = name

        parameters['name'] = name

        self.parameters = parameters

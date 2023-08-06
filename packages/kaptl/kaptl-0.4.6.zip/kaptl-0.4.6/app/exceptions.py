class MSBuildNotFoundException(Exception):
    pass


class MSBuildFailedException(Exception):
    pass


class NoStackInfoException(Exception):
    pass


class WrongStackInfoException(Exception):
    pass


class NoRulesInfoException(Exception):
    pass


class NotKaptlProjectException(Exception):
    pass

class RulesFileNotFound(Exception):
    pass
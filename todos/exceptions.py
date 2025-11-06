"""
Those errors are so generic that it might be worth to move them to some generic directory
"""
class InstanceAlreadyExistsError(Exception):
    pass


class InstanceNotFoundError(Exception):
    pass


class UniqueConstraintViolatedError(Exception):
    pass

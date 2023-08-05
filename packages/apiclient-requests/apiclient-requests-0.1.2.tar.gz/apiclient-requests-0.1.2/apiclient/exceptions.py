

class ApiException(Exception):

    def __int__(self, message):
        super(ApiException, self).__init__()
        self.message = message

    def get_message(self):
        return self.message


class NotAuthorisedException(ApiException):

    def __init__(self, message):
        super(NotAuthorisedException, self).__init__(message)


class NotFoundException(ApiException):

    def __init__(self, message):
        super(NotFoundException, self).__init__(message)


class ForbiddenException(ApiException):

    def __init__(self, message):
        super(ForbiddenException, self).__init__(message)


class InternalServerError(ApiException):

    def __init__(self, message):
        super(InternalServerError, self).__init__(message)
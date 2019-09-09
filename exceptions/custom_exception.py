from http import HTTPStatus


class CustomException(Exception):
    def __init__(self, message):
        super(CustomException, self).__init__(message)
        self.message = message
        self.status_code = HTTPStatus.BAD_REQUEST

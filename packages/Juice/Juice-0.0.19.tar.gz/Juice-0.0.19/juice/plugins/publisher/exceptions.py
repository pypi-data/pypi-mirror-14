

from juice.exceptions import HTTPException

class PublisherPageNotFound(HTTPException):
    code = 404
    description = "This content doesn't exist"






class UnknownUserException(Exception):
    'Raised when the username is not in the Training Data'
    pass



class UserIdAbsetInNewDataError(Exception):
    'Raise when an expected user id is absent in the new data'
    pass
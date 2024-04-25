from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code,
                         detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="User already exist in database"


class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect email or password"


class TokenExpriredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Your token is expired"


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token is missing"


class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect format of token"


class UserAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Unauthorized"


class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="There is no rooms left"

class RoomCannotBeDelete(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="You cannot delete a non-existent booking"

class HotelsCannotBeBooked(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Incorrect relation between DATE FROM and DATE TO"
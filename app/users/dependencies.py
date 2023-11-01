from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpriredException, UserAbsentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
        token, settings.AUTH_KEY, settings.AUTH_ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpriredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserAbsentException
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserAbsentException

    return user

async def get_current_admin_user(current_user: str = Depends(get_current_user)):
    return current_user

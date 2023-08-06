from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app import schemas
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.AWS_DEV_TOKEN_URL)


def get_auth_user(token: str = Depends(oauth2_scheme)):
    verifications = {'signature', 'aud', 'iat', 'exp', 'nbf', 'iss', 'sub', 'jti', 'at_hash'}
    no_verification = {f'verify_{x}': False for x in verifications}
    # print('received auth token', token)
    payload = jwt.decode(token, 'NO SECRET', algorithms=['RS256'], options=no_verification)
    return schemas.AuthUser(**payload)


def get_header(requests: Request):
    headers = {'authorization': requests.headers['authorization'],
               'accept': requests.headers['accept']}

    return headers

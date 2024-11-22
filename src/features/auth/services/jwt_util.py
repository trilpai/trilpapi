from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload to include in the JWT.
        expires_delta (timedelta, optional): Expiry duration for the token. Defaults to settings.jwt_expiration_minutes.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expiration_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT refresh token.

    Args:
        data (dict): The payload to include in the JWT.
        expires_delta (timedelta, optional): Expiry duration for the token. Defaults to 7 days.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodes and verifies a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        decoded_jwt = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return decoded_jwt
    except JWTError as e:
        raise ValueError("Invalid or expired token") from e

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from src.features.auth.services.auth_service import authenticate_user

# Define the router
router = APIRouter()

# Request schema for user signin
class SigninRequest(BaseModel):
    loginid: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "loginid": "admin",
                "password": "securepassword123"
            }
        }

# Response schema for user signin
class SigninResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1Ni...",
                "refresh_token": "eyJhbGciOiJIUzI1Ni..."
            }
        }


@router.post("/signin", response_model=SigninResponse, tags=["Authentication"])
async def signin(
    signin_data: SigninRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Handles user signin and generates access and refresh tokens.

    Args:
        signin_data (SigninRequest): Login credentials provided by the user.
        db (AsyncSession): Database session injected via dependency.

    Returns:
        SigninResponse: A dictionary containing access and refresh tokens.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    try:
        tokens = await authenticate_user(db, signin_data.loginid, signin_data.password)
        return SigninResponse(**tokens)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

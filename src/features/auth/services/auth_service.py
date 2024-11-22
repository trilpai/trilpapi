from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.features.users.models.users import User
from src.features.auth.services.jwt_util import create_access_token, create_refresh_token
from src.core.security import verify_hash
from datetime import timedelta


async def authenticate_user(session: AsyncSession, loginid: str, password: str) -> dict:
    """
    Authenticates the user by login ID and password.

    Args:
        session (AsyncSession): Database session.
        loginid (str): Login ID of the user.
        password (str): Plaintext password.

    Returns:
        dict: A dictionary containing the user's information and tokens if authentication succeeds.

    Raises:
        ValueError: If authentication fails.
    """
    # Fetch the user by login ID
    query = select(User).where(User.loginid == loginid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_hash(password, user.password):
        raise ValueError("Invalid login credentials")

    # Create JWT tokens
    user_data = {
        "userid": user.id,
        "loginid": user.loginid,
        "name": user.name,
        "gender": user.gender,
        "profile_pic_url": user.profile_pic_url,
        "lang_pref": user.lang_pref,
        "tzone": user.tzone,
        "role": user.role,
        "privileges": [],  # Placeholder for privileges
        "office": user.office,
        "job_title": user.job_title,
    }

    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    return {"access_token": access_token, "refresh_token": refresh_token}

from passlib.context import CryptContext

# Initialize the bcrypt context for hashing and verifying
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(text: str) -> str:
    """
    Hashes a plaintext string using bcrypt.

    This function can be used to hash any plaintext text, such as passwords or OTPs.

    Args:
        text (str): The plaintext string to be hashed (e.g., password, OTP).

    Returns:
        str: The hashed version of the input text.
    """
    return pwd_context.hash(text)


def verify_hash(plain_text: str, hashed_text: str) -> bool:
    """
    Verifies if a plaintext string matches its hashed version.

    This function can be used to verify both passwords and OTPs.

    Args:
        plain_text (str): The plaintext string to verify (e.g., password, OTP).
        hashed_text (str): The hashed version of the string.

    Returns:
        bool: True if the plaintext matches the hashed text, False otherwise.
    """
    return pwd_context.verify(plain_text, hashed_text)

from pydantic_settings import BaseSettings
from src.core.constants import PROJECT_ROOT
import base64


class Settings(BaseSettings):
    """
    Manages application configuration using environment variables or a `.env` file.

    This class handles essential application settings such as database connection URLs,
    JWT secrets, and environment information. It ensures secure decoding of sensitive
    information and validates critical configurations.

    Attributes:
        app_name (str): Name of the application.
        database_url (str): Database connection URL for SQLAlchemy.
        jwt_secret (str): Secret key for JWT signing and verification.
        jwt_algorithm (str): Algorithm used for JWT encoding (default: "HS256").
        jwt_expiration_minutes (int): JWT expiration time in minutes (default: 30).
        env (str): Current environment (e.g., "development", "production").
    """

    # Define configuration attributes
    app_name: str = "Trilp API"
    log_level: str = "INFO"  # Default log level if not provided in .env
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    env: str = "development"  # Indicates the current environment (e.g., development, production)

    class Config:
        """
        Pydantic configuration for the Settings class.

        Attributes:
            env_file (str): Path to the `.env` file used for environment variables.
        """
        env_file = str(PROJECT_ROOT / ".env")

    def __init__(self, **kwargs):
        """
        Initializes the settings object, decodes sensitive data if necessary,
        and validates required configurations.

        Args:
            **kwargs: Optional keyword arguments passed to the BaseSettings initializer.
        """
        super().__init__(**kwargs)

        # Decode JWT secret if it starts with "base64:"
        if self.jwt_secret.startswith("base64:"):
            try:
                encoded_secret = self.jwt_secret[len("base64:"):]
                self.jwt_secret = base64.b64decode(encoded_secret).decode("utf-8")
            except Exception as e:
                raise ValueError("Invalid Base64 encoding for JWT_SECRET.") from e

        # Validate essential configurations
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL is not set. Please check your `.env` file or environment variables."
            )
        if not self.jwt_secret:
            raise ValueError(
                "JWT_SECRET is not set. Please check your `.env` file or environment variables."
            )


# Instantiate the settings object for use throughout the application
settings = Settings()

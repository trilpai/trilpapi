from sqlalchemy import Column, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime


class RefreshToken(Base):
    """
    Represents a refresh token for a user.

    Refresh tokens are used to obtain new access tokens without requiring the user to re-authenticate.
    They are securely hashed and associated with a user.
    """
    __tablename__ = "refresh_tokens"

    # Columns
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        doc="Unique identifier for the refresh token record."
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        doc="References the user to whom the refresh token belongs."
    )
    token = Column(
        String(255),
        nullable=False,
        doc="Securely hashed refresh token value to prevent tampering or misuse."
    )
    expires_at = Column(
        DateTime,
        nullable=False,
        doc="Timestamp indicating when the refresh token expires."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the refresh token was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the refresh token was last updated."
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="refresh_tokens",
        doc="Defines the relationship with the User model."
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return f"<RefreshToken(id={self.id!r}, user_id={self.user_id!r})>"

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.

        Returns:
            dict: A dictionary representation of the RefreshToken instance.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

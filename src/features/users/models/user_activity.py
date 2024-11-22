from sqlalchemy import Column, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime


class UserActivity(Base):
    """
    Represents a user's activity in the system.

    This table tracks various actions performed by users, including their metadata such as
    IP address and user agent.
    """
    __tablename__ = "user_activity"

    # Columns
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        doc="Unique identifier for the user activity record."
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        doc="References the user who performed the action."
    )
    action = Column(
        String(32),
        nullable=False,
        doc="Specifies the type of action (e.g., LOGIN, LOGOUT, FAILED_LOGIN, PASSWORD_CHANGE)."
    )
    action_time = Column(
        DateTime,
        nullable=False,
        doc="Timestamp of when the action was performed."
    )
    ip_address = Column(
        String(48),
        nullable=True,
        doc="Tracks the IP address of the user; supports both IPv4 and IPv6."
    )
    user_agent = Column(
        String(255),
        nullable=True,
        doc="Stores the user agent string of the device used to perform the action."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the user activity record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the user activity record was last updated."
    )

    # Relationships
    user = relationship(
        "User",
        back_populates="user_activity",
        doc="Defines the relationship with the User model."
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return f"<UserActivity(id={self.id!r}, user_id={self.user_id!r}, action={self.action!r})>"

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.

        Returns:
            dict: A dictionary representation of the UserActivity instance.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "action_time": self.action_time.isoformat() if self.action_time else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

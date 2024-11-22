from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime


class Privilege(Base):
    """
    Represents a privilege in the system.

    Privileges define granular access rights within the system, such as the ability
    to perform specific actions or access certain resources.
    """
    __tablename__ = "privileges"

    # Columns
    privilege = Column(
        String(24),
        primary_key=True,
        nullable=False,
        doc="Unique identifier for the privilege, generated using a custom strategy "
            "(e.g., 'USER_R', 'USER_W', 'USER_D')."
    )
    tag = Column(
        String(24),
        nullable=True,
        doc="Optional categorization or grouping tag for the privilege "
            "(e.g., 'USER_MANAGEMENT')."
    )
    description = Column(
        String(64),
        nullable=True,
        doc="A brief description of what the privilege allows (e.g., 'Allows creating users')."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the privilege record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the privilege record was last updated."
    )

    # Relationships
    role_privileges = relationship(
        "RolePrivilege",
        back_populates="privilege",
        cascade="all, delete-orphan",  # Automatically delete related RolePrivilege entries
        doc="Defines the relationship with RolePrivilege model entries associated with this privilege."
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return f"<Privilege(privilege={self.privilege!r}, tag={self.tag!r})>"

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.

        Returns:
            dict: A dictionary representation of the Privilege instance.
        """
        return {
            "privilege": self.privilege,
            "tag": self.tag,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

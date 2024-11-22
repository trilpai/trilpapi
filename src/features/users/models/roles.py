from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime


class Role(Base):
    """
    Represents a role in the system.

    Roles define a user's level of access and permissions within the system,
    typically linked to one or more privileges.
    """
    __tablename__ = "roles"

    # Columns
    role = Column(
        String(24),
        primary_key=True,
        nullable=False,
        doc="Unique identifier for the role, generated using a custom strategy (e.g., 'ADMIN', 'USER')."
    )
    description = Column(
        String(64),
        nullable=True,
        doc="A brief description of the role's purpose or permissions."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the role record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the role record was last updated."
    )

    # Relationships
    role_privileges = relationship(
        "RolePrivilege",
        back_populates="role",
        cascade="all, delete-orphan",  # Automatically delete related RolePrivilege entries
        doc="Defines the relationship with RolePrivilege model entries associated with this role."
    )
    users = relationship(
        "User",
        back_populates="role",
        passive_deletes=True,  # Set foreign key to NULL on delete
        doc="Defines the relationship with User model entries associated with this role."
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return f"<Role(role={self.role!r}, description={self.description!r})>"

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.

        Returns:
            dict: A dictionary representation of the Role instance.
        """
        return {
            "role": self.role,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

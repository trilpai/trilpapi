from sqlalchemy import Column, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models.base import Base


class RolePrivilege(Base):
    """
    Represents the mapping between roles and privileges in the system.

    This table establishes a many-to-many relationship between roles and privileges.
    Each record links a role to a privilege for Role-Based Access Control (RBAC).
    """
    __tablename__ = "role_privileges"

    # Define columns
    role = Column(
        String(24),
        ForeignKey("roles.role", ondelete="CASCADE"),
        nullable=False,
        doc="The role associated with this privilege. "
            "Links to the 'role' field in the 'roles' table."
    )
    privilege = Column(
        String(24),
        ForeignKey("privileges.privilege", ondelete="CASCADE"),
        nullable=False,
        doc="The privilege associated with this role. "
            "Links to the 'privilege' field in the 'privileges' table."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the record was last updated."
    )

    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint("role", "privilege", name="pk_role_privilege"),
    )

    # Define relationships
    role_relationship = relationship(
        "Role",
        back_populates="role_privileges",
        doc="Relationship to the Role model."
    )
    privilege_relationship = relationship(
        "Privilege",
        back_populates="role_privileges",
        doc="Relationship to the Privilege model."
    )

    def __repr__(self):
        """
        Returns a string representation of the RolePrivilege instance.

        Example:
            <RolePrivilege(role='admin', privilege='view_reports')>
        """
        return f"<RolePrivilege(role={self.role!r}, privilege={self.privilege!r})>"

    def to_dict(self):
        """
        Converts the RolePrivilege instance to a dictionary for JSON serialization.

        Returns:
            dict: A dictionary representation of the RolePrivilege instance.
        """
        return {
            "role": self.role,
            "privilege": self.privilege,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

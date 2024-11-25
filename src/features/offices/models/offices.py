from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Float,
    Index,
    DECIMAL,
    ForeignKeyConstraint,
    event,
)
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime
from src.features.users.models.users import User


class Office(Base):
    """
    Represents an office entity.
    """
    __tablename__ = "offices"  # Explicit table name

    # Columns
    code = Column(
        String(16),
        primary_key=True,
        nullable=False,
        unique=True,
        doc="Unique identifier for the office, generated using a custom strategy."
    )
    name = Column(
        String(48),
        nullable=False,
        doc="Name of the office (e.g., 'Headquarters', 'Branch Office')."
    )
    o_type = Column(
        String(24),
        nullable=False,
        doc="Type of office, restricted to values: 'HQ' (Headquarters) or 'BRANCH'."
    )
    ph_num1 = Column(
        String(16),
        nullable=True,
        doc="Primary phone number for the office."
    )
    ph_num2 = Column(
        String(16),
        nullable=True,
        doc="Secondary phone number for the office."
    )
    email1 = Column(
        String(48),
        nullable=True,
        doc="Primary email address for the office."
    )
    email2 = Column(
        String(48),
        nullable=True,
        doc="Secondary email address for the office."
    )
    website = Column(
        String(48),
        nullable=True,
        doc="Website address of the office, if any."
    )
    gst_num = Column(
        String(24),
        nullable=True,
        doc="GST number of the office, if any."
    )
    pincode = Column(
        String(8),
        nullable=True,
        doc="Pincode or postal code of the office location."
    )
    country = Column(
        String(48),
        nullable=True,
        doc="Country where the office is located."
    )
    state = Column(
        String(48),
        nullable=True,
        doc="State or province of the office location."
    )
    district = Column(
        String(48),
        nullable=True,
        doc="District where the office is situated."
    )
    taluka = Column(
        String(48),
        nullable=True,
        doc="Sub-district or taluka of the office location."
    )
    place = Column(
        String(48),
        nullable=True,
        doc="City, town, village, or place name for the office."
    )
    address_line1 = Column(
        String(64),
        nullable=True,
        doc="First line of the office address (e.g., street name or number)."
    )
    address_line2 = Column(
        String(64),
        nullable=True,
        doc="Second line of the office address (e.g., apartment or suite)."
    )
    address_line3 = Column(
        String(64),
        nullable=True,
        doc="Third line of the office address (optional for extra details)."
    )
    o_lat = Column(
        DECIMAL(11, 8),
        nullable=True,
        doc="Latitude coordinates for the office location."
    )
    o_long = Column(
        DECIMAL(11, 8),
        nullable=True,
        doc="Longitude coordinates for the office location."
    )
    notes = Column(
        String(64),
        nullable=True,
        doc="Additional notes or comments about the office."
    )
    active = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates whether the office is active (true) or inactive (false)."
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
        doc="Timestamp for soft deletes; null if the record is active."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the office record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the office record was last updated."
    )

    # Relationships
    users = relationship(
        "User",
        back_populates="office",
        cascade="all, delete-orphan",  # Ensure dependent users are updated/nullified on soft delete
        passive_deletes=True,
        doc="Defines the relationship with the User model."
    )

    # Indexes
    __table_args__ = (
        Index("ix_offices_o_type", "o_type"),  # Index for filtering by o_type
        Index("ix_offices_active", "active"),  # Index for filtering by active status
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return (
            f"<Office(code={self.code!r}, name={self.name!r}, "
            f"type={self.o_type!r}, active={self.active!r})>"
        )

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.
        """
        return {
            "code": self.code,
            "name": self.name,
            "o_type": self.o_type,
            "ph_num1": self.ph_num1,
            "ph_num2": self.ph_num2,
            "email1": self.email1,
            "email2": self.email2,
            "website": self.website,
            "gst_num": self.gst_num,
            "pincode": self.pincode,
            "country": self.country,
            "state": self.state,
            "district": self.district,
            "taluka": self.taluka,
            "place": self.place,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "address_line3": self.address_line3,
            "o_lat": float(self.o_lat) if self.o_lat is not None else None,
            "o_long": float(self.o_long) if self.o_long is not None else None,
            "notes": self.notes,
            "active": self.active,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Event listener to handle soft delete and nullify related foreign keys
@event.listens_for(Office, "before_delete")
def before_delete(mapper, connection, target):
    """
    Handles actions before deleting an Office, such as nullifying related foreign keys.
    """
    connection.execute(
        """
        UPDATE users
        SET office = NULL
        WHERE office = :office_code
        """,
        {"office_code": target.code},
    )

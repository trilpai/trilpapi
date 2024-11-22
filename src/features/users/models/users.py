from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer, ForeignKey, event
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.features.users.models.refresh_tokens import RefreshToken
from src.features.users.models.user_activity import UserActivity
from datetime import datetime


class User(Base):
    """
    Represents a user in the system.

    Users are entities with specific roles and privileges, and they may belong to an office.
    They can authenticate via login ID, mobile number, email, or third-party integrations.
    """
    __tablename__ = "users"

    # Columns
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        doc="Unique identifier for the user."
    )
    loginid = Column(
        String(16),
        unique=True,
        nullable=False,
        doc="Manually generated login ID, username, or employee ID for user authentication."
    )
    mobile = Column(
        String(16),
        nullable=True,
        doc="Registered mobile number; can also be used for login."
    )
    email = Column(
        String(48),
        nullable=True,
        doc="Registered email address; can also be used for login."
    )
    google_id = Column(
        String(128),
        nullable=True,
        doc="Google ID for users logging in with Google authentication."
    )
    password = Column(
        String(255),
        nullable=True,
        doc="Hashed password stored securely using bcrypt."
    )
    last_passwd_change = Column(
        DateTime,
        nullable=True,
        doc="Date and time of the last password change to enforce periodic password updates."
    )
    otp = Column(
        String(255),
        nullable=True,
        doc="Hashed OTP for mobile verification."
    )
    otp_gen_at = Column(
        DateTime,
        nullable=True,
        doc="Date and time when the OTP was generated; restricts OTP generation to every 2 minutes."
    )
    name = Column(
        String(48),
        nullable=False,
        doc="Full name of the user."
    )
    dob = Column(
        DateTime,
        nullable=True,
        doc="Date of birth of the user."
    )
    gender = Column(
        String(16),
        nullable=True,
        doc="Gender of the user; must be one of: MALE, FEMALE, TRANSGENDER."
    )
    profile_pic_url = Column(
        String(255),
        nullable=True,
        doc="URL to the user's profile picture stored in the file system."
    )
    lang_pref = Column(
        String(16),
        nullable=True,
        doc="User's preferred language for communication (e.g., EN, FR, ES)."
    )
    tzone = Column(
        String(64),
        nullable=True,
        doc="User's preferred timezone for scheduling and timestamp handling."
    )
    role = Column(
        String(24),
        ForeignKey("roles.role", ondelete="SET NULL"),
        nullable=True,
        doc="Role assigned to the user (e.g., ADMIN, USER)."
    )
    office = Column(
        String(16),
        ForeignKey("offices.code", ondelete="SET NULL"),
        nullable=True,
        doc="Office code associated with the user."
    )
    job_title = Column(
        String(24),
        nullable=True,
        doc="Job title of the user (e.g., Manager, Developer)."
    )
    mobile_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates if the registered mobile number is verified."
    )
    email_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates if the registered email address is verified."
    )
    email_verification_otp = Column(
        String(255),
        nullable=True,
        doc="Hashed OTP for email verification purposes."
    )
    email_otp_gen_at = Column(
        DateTime,
        nullable=True,
        doc="Date and time when the email OTP was generated; restricts generation to every 2 minutes."
    )
    jwtoken = Column(
        String(255),
        nullable=True,
        doc="Hashed active JWT for invalidation purposes."
    )
    last_login_at = Column(
        DateTime,
        nullable=True,
        doc="Tracks the date and time of the last successful login."
    )
    last_failed_at = Column(
        DateTime,
        nullable=True,
        doc="Tracks the date and time of the last failed login attempt."
    )
    failed_attempts = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Tracks the number of failed login attempts."
    )
    lockout_until = Column(
        DateTime,
        nullable=True,
        doc="Timestamp indicating when the user's account will be unlocked."
    )
    is_locked = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates if the user's account is locked due to multiple failed login attempts."
    )
    active = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates if the user's account is active or deactivated."
    )
    created_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
        doc="ID of the user who created this record (self-referential)."
    )
    updated_by = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
        doc="ID of the user who last updated this record (self-referential)."
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
        doc="Timestamp for soft delete; null if the record is active."
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the user record was created."
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp of when the user record was last updated."
    )

    # Relationships
    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        doc="Defines the relationship with RefreshToken model entries associated with this user."
    )

    user_activity = relationship(
        "UserActivity",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        doc="Defines the relationship with UserActivity model entries associated with this user."
    )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging.
        """
        return f"<User(id={self.id!r}, loginid={self.loginid!r}, active={self.active!r})>"

    def to_dict(self):
        """
        Converts the object to a dictionary for JSON serialization or API responses.

        Returns:
            dict: A dictionary representation of the User instance.
        """
        return {
            "id": self.id,
            "loginid": self.loginid,
            "mobile": self.mobile,
            "email": self.email,
            "google_id": self.google_id,
            "last_passwd_change": self.last_passwd_change.isoformat() if self.last_passwd_change else None,
            "otp_gen_at": self.otp_gen_at.isoformat() if self.otp_gen_at else None,
            "name": self.name,
            "dob": self.dob.isoformat() if self.dob else None,
            "gender": self.gender,
            "profile_pic_url": self.profile_pic_url,
            "lang_pref": self.lang_pref,
            "tzone": self.tzone,
            "role": self.role,
            "office": self.office,
            "job_title": self.job_title,
            "mobile_verified": self.mobile_verified,
            "email_verified": self.email_verified,
            "email_otp_gen_at": self.email_otp_gen_at.isoformat() if self.email_otp_gen_at else None,
            "jwtoken": self.jwtoken,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "last_failed_at": self.last_failed_at.isoformat() if self.last_failed_at else None,
            "failed_attempts": self.failed_attempts,
            "lockout_until": self.lockout_until.isoformat() if self.lockout_until else None,
            "is_locked": self.is_locked,
            "active": self.active,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

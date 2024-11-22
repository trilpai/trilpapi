"""Seed initial privilege, role, and user data

Revision ID: 883edf75f2a1
Revises: 0e7b7745d909
Create Date: 2024-11-21 13:23:55.453629

"""
from typing import Sequence, Union
from alembic import op
from src.core.security import get_hash  # Import the password hashing function


# revision identifiers, used by Alembic.
revision: str = '883edf75f2a1'
down_revision: Union[str, None] = '0e7b7745d909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Insert initial data for privileges, roles, role_privileges, and users with hashed passwords.
    """
    # Hash the password using bcrypt
    raw_password = "1234"  # Original password
    hashed_password = get_hash(raw_password)

    # Insert data
    op.execute(
        """
        INSERT INTO `privileges` 
        (`privilege`, `tag`, `description`, `created_at`, `updated_at`) 
        VALUES 
        ('SYS_ALL', 'System Admin', 'Full system access privilege. Please be careful.', NOW(), NOW());
        """
    )
    op.execute(
        """
        INSERT INTO `roles` 
        (`role`, `description`, `created_at`, `updated_at`) 
        VALUES 
        ('SYSTEM ADMIN', 'System Administrator role with root or super user privileges.', NOW(), NOW());
        """
    )
    op.execute(
        """
        INSERT INTO `role_privileges` 
        (`role`, `privilege`, `created_at`, `updated_at`) 
        VALUES 
        ('SYSTEM ADMIN', 'SYS_ALL', NOW(), NOW());
        """
    )
    op.execute(
        f"""
        INSERT INTO `users` 
        (`loginid`, `mobile`, `email`, `password`, `name`, `role`, `job_title`, 
        `mobile_verified`, `email_verified`, `failed_attempts`, `is_locked`, `active`, `created_at`, `updated_at`) 
        VALUES 
        ('admin', '9876543210', 'admin@comp.com', '{hashed_password}', 'System Admin', 
        'SYSTEM ADMIN', 'System Admin', 0, 0, 0, 0, 1, NOW(), NOW());
        """
    )


def downgrade() -> None:
    """
    Remove the seeded data for privileges, roles, role_privileges, and users in reverse order.
    """
    op.execute(
        """
        DELETE FROM `users` 
        WHERE `loginid` = 'admin' AND `role` = 'SYSTEM ADMIN';
        """
    )
    op.execute(
        """
        DELETE FROM `role_privileges` 
        WHERE `role` = 'SYSTEM ADMIN' AND `privilege` = 'SYS_ALL';
        """
    )
    op.execute(
        """
        DELETE FROM `roles` 
        WHERE `role` = 'SYSTEM ADMIN';
        """
    )
    op.execute(
        """
        DELETE FROM `privileges` 
        WHERE `privilege` = 'SYS_ALL';
        """
    )

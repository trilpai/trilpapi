"""Create roles and role_privileges table

Revision ID: 0b88cf63cd67
Revises: cb664f2bb93c
Create Date: 2024-11-21 11:47:42.888260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b88cf63cd67'
down_revision: Union[str, None] = 'cb664f2bb93c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('role', sa.String(length=24), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('role')
    )
    op.create_table('role_privileges',
    sa.Column('role', sa.String(length=24), nullable=False),
    sa.Column('privilege', sa.String(length=24), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['privilege'], ['privileges.privilege'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role'], ['roles.role'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('role', 'privilege', name='pk_role_privilege')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role_privileges')
    op.drop_table('roles')
    # ### end Alembic commands ###

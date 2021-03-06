"""add field role to user table

Revision ID: 875fb7a3cf08
Revises: 936cd9ae64a6
Create Date: 2020-07-25 22:16:08.710775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875fb7a3cf08'
down_revision = '936cd9ae64a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.String(length=30), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###

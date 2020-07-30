"""add count_likes for user table

Revision ID: 402cbbe662f9
Revises: 0f49b04c0eb0
Create Date: 2020-07-30 00:19:25.806820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '402cbbe662f9'
down_revision = '0f49b04c0eb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('count_likes', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('count_recipes', sa.Integer(), nullable=True))
    op.drop_column('users', 'count_recipe')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('count_recipe', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('users', 'count_recipes')
    op.drop_column('users', 'count_likes')
    # ### end Alembic commands ###
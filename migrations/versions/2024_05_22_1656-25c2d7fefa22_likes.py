"""likes

Revision ID: 25c2d7fefa22
Revises: 
Create Date: 2024-05-22 16:56:08.347340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25c2d7fefa22'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_login', sa.String(), nullable=False),
    sa.Column('who_i_liked', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_login'], ['users.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('who_liked_me',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_login', sa.String(), nullable=True),
    sa.Column('user_who_was_liked', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_login'], ['users.login'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes_to_likes_association_table',
    sa.Column('my_likes_id', sa.Integer(), nullable=False),
    sa.Column('who_liked_me_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['my_likes_id'], ['my_likes.id'], ),
    sa.ForeignKeyConstraint(['who_liked_me_id'], ['who_liked_me.id'], ),
    sa.PrimaryKeyConstraint('my_likes_id', 'who_liked_me_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes_to_likes_association_table')
    op.drop_table('who_liked_me')
    op.drop_table('my_likes')
    # ### end Alembic commands ###

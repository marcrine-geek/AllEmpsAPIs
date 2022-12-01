"""empty message

Revision ID: a0c2ebed5589
Revises: 
Create Date: 2022-12-01 09:00:18.197403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0c2ebed5589'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('channel_name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('channel_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('post', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_posts')
    op.drop_table('followers')
    op.drop_table('channel_posts')
    op.drop_table('channel_members')
    op.drop_table('users')
    op.drop_table('channels')
    # ### end Alembic commands ###

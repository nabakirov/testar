"""empty message

Revision ID: e7ec2aa74b8f
Revises: 7c894a8ecac6
Create Date: 2018-04-28 12:03:41.283682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ec2aa74b8f'
down_revision = '7c894a8ecac6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'question', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_column('question', 'user_id')
    # ### end Alembic commands ###

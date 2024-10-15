"""created table groups

Revision ID: 36a665f71d5c
Revises: d9ce8b380f3e
Create Date: 2024-10-15 11:26:41.064469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36a665f71d5c'
down_revision = 'd9ce8b380f3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('email', sa.String(length=225), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    op.drop_table('groups')
    # ### end Alembic commands ###
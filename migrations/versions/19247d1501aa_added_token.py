"""added token

Revision ID: 19247d1501aa
Revises: a38701cd20ea
Create Date: 2024-10-18 09:36:52.440418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19247d1501aa'
down_revision = 'a38701cd20ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_block_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('token_block_list', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_block_list_jti'), ['jti'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_block_list', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_block_list_jti'))

    op.drop_table('token_block_list')
    # ### end Alembic commands ###

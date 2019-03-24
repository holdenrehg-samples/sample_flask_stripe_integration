"""empty message

Revision ID: 8532d8890ba0
Revises: 
Create Date: 2019-03-23 16:25:53.949394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8532d8890ba0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_four', sa.String(length=4), nullable=False))
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('stripe_token', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'stripe_token')
    op.drop_column('users', 'stripe_customer_id')
    op.drop_column('users', 'last_four')
    # ### end Alembic commands ###
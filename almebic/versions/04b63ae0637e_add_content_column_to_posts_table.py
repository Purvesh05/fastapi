"""add content column to posts table

Revision ID: 04b63ae0637e
Revises: 7f423ff9998d
Create Date: 2023-08-05 14:53:45.929979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04b63ae0637e'
down_revision = '7f423ff9998d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass

"""Create posts table

Revision ID: 7f423ff9998d
Revises: 
Create Date: 2023-08-05 13:38:58.054095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f423ff9998d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer,nullable=False,primary_key=True),sa.Column('Title',sa.String,nullable=False))
    

def downgrade() -> None:
    op.drop_table('posts')
    pass

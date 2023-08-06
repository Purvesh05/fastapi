"""add last few columns to posts table 

Revision ID: 728c6add079d
Revises: 5e1ca712d56d
Create Date: 2023-08-05 17:54:26.634415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '728c6add079d'
down_revision = '5e1ca712d56d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),server_default='True',nullable=False),)
    op.add_column('posts',
                  sa.Column('created',sa.TIMESTAMP(),server_default=sa.text('now()'),nullable=False))
    


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    

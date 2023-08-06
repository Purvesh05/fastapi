"""aadd foreign key to posts table

Revision ID: 5e1ca712d56d
Revises: ecda1997aba4
Create Date: 2023-08-05 17:21:34.958904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e1ca712d56d'
down_revision = 'ecda1997aba4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    

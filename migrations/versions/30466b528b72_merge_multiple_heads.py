"""Merge multiple heads

Revision ID: 30466b528b72
Revises: 4e12b169c0ad, 1234567890ab
Create Date: 2025-05-08 15:35:16.266915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30466b528b72'
down_revision = ('4e12b169c0ad', '1234567890ab')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

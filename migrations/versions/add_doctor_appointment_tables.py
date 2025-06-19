"""Add Doctor and Appointment tables

Revision ID: 1234567890ab
Revises:
Create Date: 2025-05-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1234567890ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create doctors table
    op.create_table('doctor',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=150), nullable=False),
                    sa.Column('specialty', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Create appointments table
    op.create_table('appointment',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('doctor_id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.Date(), nullable=False),
                    sa.Column('time_slot', sa.String(length=50), nullable=False),
                    sa.Column('status', sa.String(length=20), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('appointment')
    op.drop_table('doctor')
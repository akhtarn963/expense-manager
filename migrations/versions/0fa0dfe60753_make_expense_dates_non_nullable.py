"""Make expense dates non-nullable

Revision ID: 0fa0dfe60753
Revises: 07cbc24f111f
Create Date: 2026-08-06 21:36:00.227961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa0dfe60753'
down_revision = '07cbc24f111f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "expense_date",
            existing_type=sa.Date(),
            nullable=False
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False
        )

def downgrade():
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "expense_date",
            existing_type=sa.Date(),
            nullable=True
        )
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=True
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=True
        )
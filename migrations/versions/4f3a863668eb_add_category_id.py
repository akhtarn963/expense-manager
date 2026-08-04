"""Add category_id

Revision ID: 4f3a863668eb
Revises: 26fc20caf126
Create Date: 2026-08-04 20:36:05.439748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f3a863668eb'
down_revision = '26fc20caf126'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("categories") as batch_op:
        batch_op.create_unique_constraint(
            "uq_categories_name",
            ["name"]
        )

    with op.batch_alter_table("expenses") as batch_op:
        batch_op.add_column(
            sa.Column(
                "category_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_expenses_category_id",
            "categories",
            ["category_id"],
            ["id"]
        )


def downgrade():

    with op.batch_alter_table("expenses") as batch_op:
        batch_op.drop_constraint(
            "fk_expenses_category_id",
            type_="foreignkey"
        )
        batch_op.drop_column("category_id")

    with op.batch_alter_table("categories") as batch_op:
        batch_op.drop_constraint(
            "uq_categories_name",
            type_="unique"
        )

    # ### end Alembic commands ###

"""create table books

Revision ID: 01720b4dcac9
Revises: 
Create Date: 2024-11-20 22:05:59.687878

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "01720b4dcac9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("author", sa.String(length=30), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("IN_STOCK", "CHECKED_OUT", name="bookstatus"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
        sa.UniqueConstraint("title", name=op.f("uq_books_title")),
    )


def downgrade() -> None:
    op.drop_table("books")

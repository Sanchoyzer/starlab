"""
Init.

Revision ID: c5aa00c7a111
Revises:
Create Date: 2023-11-19 13:01:50.284807

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c5aa00c7a111'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS library')
    op.create_table(
        'book',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('published_at', sa.Date(), nullable=False),
        sa.Column(
            'genre',
            sa.Enum(
                'NOVEL',
                'DETECTIVE',
                'FANTASY',
                'SCIENCE_FICTION',
                'HORROR',
                'ADVENTURE',
                'POPULAR_SCIENCE',
                'RELIGIOUS_LITERATURE',
                'NON_FICTION',
                'POETRY',
                name='genretype',
            ),
            nullable=False,
        ),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column(
            'available_for_view',
            sa.Boolean(),
            server_default=sa.text('true'),
            nullable=False,
        ),
        sa.Column(
            'available_for_download',
            sa.Boolean(),
            server_default=sa.text('true'),
            nullable=False,
        ),
        sa.Column('uid', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('uid'),
        schema='library',
    )
    op.create_index(
        op.f('ix_library_book_author'),
        'book',
        ['author'],
        unique=False,
        schema='library',
    )
    op.create_index(
        op.f('ix_library_book_genre'),
        'book',
        ['genre'],
        unique=False,
        schema='library',
    )
    op.create_index(op.f('ix_library_book_name'), 'book', ['name'], unique=False, schema='library')


def downgrade() -> None:
    op.drop_index(op.f('ix_library_book_name'), table_name='book', schema='library')
    op.drop_index(op.f('ix_library_book_genre'), table_name='book', schema='library')
    op.drop_index(op.f('ix_library_book_author'), table_name='book', schema='library')
    op.drop_table('book', schema='library')
    op.execute('DROP SCHEMA IF EXISTS library')

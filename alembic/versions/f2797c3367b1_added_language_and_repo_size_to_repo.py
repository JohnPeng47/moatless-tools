"""added language and repo_size to Repo

Revision ID: f2797c3367b1
Revises: da95aeecb8f1
Create Date: 2024-08-22 19:46:45.724533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2797c3367b1'
down_revision: Union[str, None] = 'da95aeecb8f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repos', sa.Column('language', sa.String(), nullable=True))
    op.add_column('repos', sa.Column('repo_size', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('repos', 'repo_size')
    op.drop_column('repos', 'language')
    # ### end Alembic commands ###

"""added relationship from CowboyUser to RepoConfig, cascade deletes

Revision ID: 529e2719b577
Revises: 13e10adf8e27
Create Date: 2024-05-31 17:37:21.980761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '529e2719b577'
down_revision: Union[str, None] = '13e10adf8e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

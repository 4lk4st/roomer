"""create tables

Revision ID: 07460fa8c7ad
Revises: 1f6e9be7abeb
Create Date: 2023-11-01 12:03:30.177154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07460fa8c7ad'
down_revision: Union[str, None] = '1f6e9be7abeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

"""create pokemon egg group

Revision ID: 63149afd0582
Revises: 0674254ac495
Create Date: 2025-04-24 11:36:40.445512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63149afd0582'
down_revision: Union[str, None] = '0674254ac495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    egg_groups = op.create_table('egg_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    egg_group_prose = op.create_table('egg_group_prose',
    sa.Column('egg_group_id', sa.Integer(), nullable=False),
    sa.Column('local_language_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['egg_group_id'], ['egg_groups.id'], ),
    sa.ForeignKeyConstraint(['local_language_id'], ['languages.id'], ),
    sa.PrimaryKeyConstraint('egg_group_id', 'local_language_id')
    )
    pokemon_egg_groups = op.create_table('pokemon_egg_groups',
    sa.Column('species_id', sa.Integer(), nullable=False),
    sa.Column('egg_group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['egg_group_id'], ['egg_groups.id'], ),
    sa.ForeignKeyConstraint(['species_id'], ['pokemon_species.id'], ),
    sa.PrimaryKeyConstraint('species_id', 'egg_group_id')
    )

    from migration.tool import load_csv

    with load_csv("egg_groups") as csv_data:
        # id,identifier
        data = [
            {
                "id": int(row["id"]),
                "identifier": row["identifier"]
            }
            for row in csv_data
        ]
        op.bulk_insert(egg_groups, data)

    with load_csv("egg_group_prose") as csv_data:
        # egg_group_id,local_language_id,name
        data = [
            {
                "egg_group_id": int(row["egg_group_id"]),
                "local_language_id": int(row["local_language_id"]),
                "name": row["name"]
            }
            for row in csv_data
        ]
        op.bulk_insert(egg_group_prose, data)

    with load_csv("pokemon_egg_groups") as csv_data:
        # species_id,egg_group_id
        data = [
            {
                "species_id": int(row["species_id"]),
                "egg_group_id": int(row["egg_group_id"])
            }
            for row in csv_data
        ]
        op.bulk_insert(pokemon_egg_groups, data)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_egg_groups')
    op.drop_table('egg_group_prose')
    op.drop_table('egg_groups')
    # ### end Alembic commands ###

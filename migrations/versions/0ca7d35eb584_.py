"""empty message

Revision ID: 0ca7d35eb584
Revises: 971abb99e2bf
Create Date: 2021-04-28 10:57:55.735829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca7d35eb584'
down_revision = '971abb99e2bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.drop_column('Venue', 'looking_for_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('looking_for_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
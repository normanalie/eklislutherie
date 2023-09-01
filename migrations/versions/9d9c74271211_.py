"""empty message

Revision ID: 9d9c74271211
Revises: c1b659e6d6a2
Create Date: 2023-09-01 16:01:15.749566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d9c74271211'
down_revision = 'c1b659e6d6a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images_article', sa.Column('name', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images_article', 'name')
    # ### end Alembic commands ###

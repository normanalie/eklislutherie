"""empty message

Revision ID: 4656c03aa1ff
Revises: 9d9c74271211
Create Date: 2023-09-01 16:48:52.547088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4656c03aa1ff'
down_revision = '9d9c74271211'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images_article', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images_article', sa.Column('name', sa.VARCHAR(length=128), nullable=False))
    # ### end Alembic commands ###
"""empty message

Revision ID: 19add00ef7a1
Revises: 4b0c6b41aa32
Create Date: 2018-04-19 11:03:22.490267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19add00ef7a1'
down_revision = '4b0c6b41aa32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'books', ['book_id'])
    op.add_column('borrows', sa.Column('returned', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'borrows', ['borrow_id'])
    op.drop_column('borrows', 'return_status')
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.add_column('borrows', sa.Column('return_status', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'borrows', type_='unique')
    op.drop_column('borrows', 'returned')
    op.drop_constraint(None, 'books', type_='unique')
    # ### end Alembic commands ###
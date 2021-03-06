"""empty message

Revision ID: 8a54c4983f9f
Revises: 
Create Date: 2018-04-28 10:04:14.272777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a54c4983f9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blacklisted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('book_title', sa.String(), nullable=False),
    sa.Column('authors', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('copies', sa.Integer(), nullable=False),
    sa.Column('edition', sa.String(), nullable=True),
    sa.Column('publisher', sa.String(), nullable=True),
    sa.Column('isnb', sa.Integer(), nullable=True),
    sa.Column('book_cover', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('book_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('tel_no', sa.String(), nullable=True),
    sa.Column('profession', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('prof_img', sa.LargeBinary(), nullable=True),
    sa.Column('DOB', sa.DateTime(), nullable=True),
    sa.Column('about_you', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('borrows',
    sa.Column('borrow_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('date_borrowed', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('return_time', sa.DateTime(), nullable=True),
    sa.Column('returned', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('borrow_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrows')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('blacklisted_tokens')
    # ### end Alembic commands ###

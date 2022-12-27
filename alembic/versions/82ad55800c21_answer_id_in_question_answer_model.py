"""answer id in question answer model

Revision ID: 82ad55800c21
Revises: a4f553004ca0
Create Date: 2022-12-27 18:56:22.751728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82ad55800c21'
down_revision = 'a4f553004ca0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question_answers', sa.Column('answer_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'question_answers', 'answers', ['answer_id'], ['id'])
    op.drop_column('question_answers', 'text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question_answers', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'question_answers', type_='foreignkey')
    op.drop_column('question_answers', 'answer_id')
    # ### end Alembic commands ###

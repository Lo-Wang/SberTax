"""Initial revision

Revision ID: 4df023e7e750
Revises: 
Create Date: 2024-11-28 11:42:57.109039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4df023e7e750'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('mcc_code', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('documents',
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('document_type', sa.String(length=50), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('upload_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('file_data', sa.LargeBinary(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('document_id')
    )
    op.create_index(op.f('ix_documents_document_id'), 'documents', ['document_id'], unique=False)
    op.create_table('logs',
    sa.Column('log_id', sa.BIGINT(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('service_name', sa.String(length=100), nullable=False),
    sa.Column('log_level', sa.String(length=20), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('request_id', sa.String(length=36), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['documents.document_id'], ),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_index(op.f('ix_logs_log_id'), 'logs', ['log_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_logs_log_id'), table_name='logs')
    op.drop_table('logs')
    op.drop_index(op.f('ix_documents_document_id'), table_name='documents')
    op.drop_table('documents')
    op.drop_table('transactions')
    # ### end Alembic commands ###

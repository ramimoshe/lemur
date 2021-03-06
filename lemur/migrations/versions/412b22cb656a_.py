"""

Revision ID: 412b22cb656a
Revises: 4c50b903d1ae
Create Date: 2016-05-17 17:37:41.210232

"""

# revision identifiers, used by Alembic.
revision = '412b22cb656a'
down_revision = '4c50b903d1ae'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_authorities',
    sa.Column('authority_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['authority_id'], ['authorities.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )
    op.create_index('roles_authorities_ix', 'roles_authorities', ['authority_id', 'role_id'], unique=True)
    op.create_table('roles_certificates',
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )
    op.create_index('roles_certificates_ix', 'roles_certificates', ['certificate_id', 'role_id'], unique=True)
    op.create_index('certificate_associations_ix', 'certificate_associations', ['domain_id', 'certificate_id'], unique=True)
    op.create_index('certificate_destination_associations_ix', 'certificate_destination_associations', ['destination_id', 'certificate_id'], unique=True)
    op.create_index('certificate_notification_associations_ix', 'certificate_notification_associations', ['notification_id', 'certificate_id'], unique=True)
    op.create_index('certificate_replacement_associations_ix', 'certificate_replacement_associations', ['certificate_id', 'certificate_id'], unique=True)
    op.create_index('certificate_source_associations_ix', 'certificate_source_associations', ['source_id', 'certificate_id'], unique=True)
    op.create_index('roles_users_ix', 'roles_users', ['user_id', 'role_id'], unique=True)

    ### end Alembic commands ###

    # migrate existing authority_id relationship to many_to_many
    conn = op.get_bind()
    for id, authority_id in conn.execute(text('select id, authority_id from roles where authority_id is not null')):
        stmt = text('insert into roles_authorities (role_id, authority_id) values (:role_id, :authority_id)')
        stmt = stmt.bindparams(role_id=id, authority_id=authority_id)
        op.execute(stmt)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('roles_users_ix', table_name='roles_users')
    op.drop_index('certificate_source_associations_ix', table_name='certificate_source_associations')
    op.drop_index('certificate_replacement_associations_ix', table_name='certificate_replacement_associations')
    op.drop_index('certificate_notification_associations_ix', table_name='certificate_notification_associations')
    op.drop_index('certificate_destination_associations_ix', table_name='certificate_destination_associations')
    op.drop_index('certificate_associations_ix', table_name='certificate_associations')
    op.drop_index('roles_certificates_ix', table_name='roles_certificates')
    op.drop_table('roles_certificates')
    op.drop_index('roles_authorities_ix', table_name='roles_authorities')
    op.drop_table('roles_authorities')
    ### end Alembic commands ###

"""init tables

Revision ID: 5656baaceae2
Revises: dc510384ab51
Create Date: 2020-11-19 17:21:43.552093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5656baaceae2'
down_revision = 'dc510384ab51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sys_menus',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sys_op_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('user_name', sa.String(length=32), nullable=True),
    sa.Column('user_ip', sa.String(length=32), nullable=True),
    sa.Column('module', sa.String(length=32), nullable=True),
    sa.Column('action', sa.String(length=32), nullable=True),
    sa.Column('req_data', sa.Text(), nullable=True),
    sa.Column('res_data', sa.Text(), nullable=True),
    sa.Column('result', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sys_op_permissions',
    sa.Column('permission', sa.String(length=32), nullable=False),
    sa.Column('label', sa.String(length=32), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('permission')
    )
    op.create_index(op.f('ix_sys_op_permissions_permission'), 'sys_op_permissions', ['permission'], unique=True)
    op.create_table('sys_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_user', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('templates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sys_menu_op_permissions',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('permission', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['sys_menus.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['permission'], ['sys_op_permissions.permission'], ondelete='CASCADE')
    )
    op.create_table('sys_role_menus',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('permission', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['sys_menus.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['permission'], ['sys_op_permissions.permission'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['sys_roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sys_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_user', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['sys_roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sys_users')
    op.drop_table('sys_role_menus')
    op.drop_table('sys_menu_op_permissions')
    op.drop_table('templates')
    op.drop_table('sys_roles')
    op.drop_index(op.f('ix_sys_op_permissions_permission'), table_name='sys_op_permissions')
    op.drop_table('sys_op_permissions')
    op.drop_table('sys_op_logs')
    op.drop_table('sys_menus')
    # ### end Alembic commands ###
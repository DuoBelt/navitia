"""Manage multi codes

Revision ID: 14e13cf7a042
Revises: 29fc422c56cb
Create Date: 2015-05-07 15:31:55.271785

"""

# revision identifiers, used by Alembic.
revision = '14e13cf7a042'
down_revision = '29fc422c56cb'

from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga
from sqlalchemy.dialects import postgresql

map_merge = []
map_merge.append({"table_name": "network", "type_name": "Network"})
map_merge.append({"table_name": "line", "type_name": "Line"})
map_merge.append({"table_name": "route", "type_name": "Route"})
map_merge.append({"table_name": "stop_area", "type_name": "StopArea"})
map_merge.append({"table_name": "stop_point", "type_name": "StopPoint"})
map_merge.append({"table_name": "vehicle_journey", "type_name": "VehicleJourney"})


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code_type',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='navitia'
    )

    op.create_table('object_code',
    sa.Column('code_type_id', sa.BIGINT(), nullable=True),
    sa.Column('object_type_id', sa.BIGINT(), nullable=True),
    sa.Column('code', sa.TEXT(), nullable=False),
    sa.Column('object_id', sa.BIGINT(), nullable=False),
    sa.ForeignKeyConstraint(['code_type_id'], [u'navitia.code_type.id'], name=u'object_code_type_id_fkey'),
    sa.ForeignKeyConstraint(['object_type_id'], [u'navitia.object_type.id'], name=u'object_type_id_fkey'),
    schema='navitia'
    )

    op.execute("INSERT INTO navitia.code_type (id, name) VALUES (0, 'external_code');")
    for table in map_merge:
        query = "INSERT INTO navitia.object_code (code_type_id, object_type_id, code, object_id) " \
                "SELECT 0, ot.id, nt.external_code, nt.id from navitia.{table} nt, object_type ot " \
                "where ot.name = '{type_name}' " \
                "and nt.external_code is not null " \
                "and nt.external_code <> '';".format(table=table["table_name"], type_name=table["type_name"])
        op.execute(query)
        op.drop_column(table["table_name"], 'external_code', schema='navitia')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    for table in map_merge:
        op.add_column(table["table_name"], sa.Column('external_code', sa.TEXT(), nullable=True), schema='navitia')
        query = "update navitia.{table} nt set external_code=aa.code " \
                "from " \
                "(select oc.code, oc.object_id from object_code oc, object_type ot " \
                "where oc.code_type_id=0 " \
                "and ot.id=oc.object_type_id " \
                "and ot.name='{type_name}')aa " \
                "where nt.id=aa.object_id".format(table=table["table_name"], type_name=table["type_name"])
        op.execute(query)
    op.drop_table('object_code', schema='navitia')
    op.drop_table('code_type', schema='navitia')
    ### end Alembic commands ###

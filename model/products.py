from sqlalchemy import Table, Column, String

import dbconfig

product_attributes_table = Table('product_attributes', dbconfig.metadata,
        Column('id', String(100), primary_key = True),
        Column('product_id', String(100), primary_key = True),
        Column('name', String(100)),
        Column('value', String(100)),
        Column('description', String(100)))

products_table = Table('products', dbconfig.metadata,
        Column('id', String(100), primary_key = True),
        Column('name', String(100)),
        Column('description', String(100)))


from sqlalchemy import Table, Column, String

import dbconfig

offers_table = Table('offers', dbconfig.metadata,
        Column('id', String(100), primary_key = True),
        Column('name', String(100)),
        Column('offer_class', String(100)),
        Column('description', String(100)))

prices_table = Table('prices', dbconfig.metadata,
        Column('id', String(100), primary_key = True),
        Column('name', String(100)),
        Column('description', String(100)),
        Column('rate', String(100)),
        Column('uom', String(100)))

offer_product_prices_table = Table('offer_product_price', dbconfig.metadata,
        Column('id', String(100), primary_key = True),
        Column('offer_id', String(100)),
        Column('product_id', String(100)),
        Column('price_id', String(100)))


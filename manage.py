import sys

import model.products
import model.offers

def create():

    from sqlalchemy import Table
    for (name, table) in vars(model.products).iteritems():
        if isinstance(table, Table):
            table.create()

    for (name, table) in vars(model.offers).iteritems():
        if isinstance(table, Table):
            table.create()


if __name__ == "__main__":
    if 'create' in sys.argv:
        create()


from model.products import products_table
from util import genid
from util import dict_to_namedtuple

from util.monad import do, Right, Left, Just
from util.dbutil import list as dblist
from util.dbutil import find as dbfind

class Product(object):

    @classmethod
    @do
    def list(cls):
        rows = dblist(products_table)
        yield rows
        yield Just ( rows >> (lambda pl:  [Product(r) for r in pl]) )

    @classmethod
    @do
    def create(cls, product_dict):

        product = dict_to_namedtuple("Product", product_dict)
        old_product = dbfind(products_table, 'name', product.name)

        if isinstance(old_product, Right):
            yield ( old_product >> (lambda v: Left("Product with name %s already exists!" % (product.name,))) )

        row = products_table.insert()
        row.execute(id = genid(), name = product.name, description = product.description)
        row = dbfind(products_table, 'name', product.name)
        yield Right( row >> (lambda v: Product(v)) )

    def __init__(self, product_row):
        self.product = product_row

    def __getitem__(self, key):
        return getattr(self.product, key)

    def __getattr__(self, key):
        return getattr(self.product, key)

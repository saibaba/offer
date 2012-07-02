from model.offers import offers_table
from util.dbutil import list as dblist
from util.dbutil import find as dbfind

from model.offers import offer_product_prices_table
from model.offers import prices_table
from model.products import products_table

from util import genid
from util import dict_to_namedtuple
from products import Product

from util.monad import do, Right, Left, Just

class Offer(object):

    @classmethod
    @do
    def list(cls):
        rows = dblist(offers_table)
        yield rows
        yield Just ( rows >> (lambda ol:  [Offer(r) for r in ol]) )

    @classmethod
    @do
    def create(cls, offer_dict):

        offer = dict_to_namedtuple("Offer", offer_dict)
        old_offer = dbfind(offers_table, 'name', offer.name)

        if isinstance(old_offer, Right):
            yield ( old_offer >> (lambda v: Left("Offer with name %s already exists!" % (offer.name,))) )

        row = offers_table.insert()
        row.execute(id = genid(), name = offer.name, description = offer.description)
        row = dbfind(offers_table, 'name', offer.name)
        yield Right( row >> (lambda v: Offer(v)) )

    def __init__(self, offer_row):
        self.offer = offer_row

    @do
    def add_product_and_price(self, product_name, price_name):
        product = yield dbfind(products_table, 'name', product_name)
        price = yield dbfind(prices_table, 'name', price_name)

        print "Using prouct:", product
        print "Using price:", price

        row = offer_product_prices_table.insert()
        row.execute(id=genid(), offer_id=self.id, product_id=product.id, price_id=price.id)
        yield Just(self)

    def products(self):
        results = []
        s = offer_product_prices_table.select(offer_product_prices_table.c.offer_id == self.offer.id)
        rs = s.execute()
        for row in rs:
            product = Product.find_by_id(row['product_id'])
            results.append(dict(offer_id=row['offer_id'], name=product.name, description=product.description))

        return results

    def __getitem__(self, key):
        return getattr(self.offer, key)

    def __getattr__(self, key):
        return getattr(self.offer, key)


class Price(object):

    @classmethod
    @do
    def list(cls):
        rows = dblist(prices_table)
        yield rows
        yield Just ( rows >> (lambda pl:  [Price(r) for r in pl]) )

    @classmethod
    @do
    def create(cls, price_dict):

        price = dict_to_namedtuple("Price", price_dict)
        old_price = dbfind(prices_table, 'name', price.name)

        if isinstance(old_price, Right):
            yield ( old_price >> (lambda v: Left("Price with name %s already exists!" % (price.name,))) )

        row = prices_table.insert()
        row.execute(id = genid(), name = price.name, description = price.description, rate=price.rate, uom=price.uom)
        row = dbfind(prices_table, 'name', price.name)
        yield Right( row >> (lambda v: Price(v)) )

    def __init__(self, price_row):
        self.price = price_row

    def __getitem__(self, key):
        return getattr(self.price, key)

    def __getattr__(self, key):
        return getattr(self.price, key)


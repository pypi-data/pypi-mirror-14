# -*- coding: utf-8 -*-
from trytond.pool import Pool
from product import Product


def register():
    Pool.register(
        Product,
        module='customs_value', type_='model'
    )

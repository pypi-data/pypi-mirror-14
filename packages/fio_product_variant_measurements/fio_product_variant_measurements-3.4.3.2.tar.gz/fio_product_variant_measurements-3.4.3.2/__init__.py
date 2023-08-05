# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from product import Product


def register():
    Pool.register(
        Product,
        module='product_variant_measurements', type_='model'
    )

# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from product import Template, Product


def register():
    Pool.register(
        Template,
        Product,
        module='product_variant', type_='model'
    )

# -*- coding: utf-8 -*-
"""
    tests/test_product.py

"""
import unittest
from decimal import Decimal
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, DB_NAME, CONTEXT
from trytond.transaction import Transaction


class TestProduct(unittest.TestCase):
    def setUp(self):
        trytond.tests.test_tryton.install_module('product_variant')

        self.ProductTemplate = POOL.get('product.template')
        self.Product = POOL.get('product.product')
        self.Uom = POOL.get('product.uom')

    def test_0010_use_variant_lp_and_cp(self):
        """Since we have moved list price and cost price to variant, any logic
        which goes for product lp and cp should raise an exception.
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):

            uom, = self.Uom.search([('symbol', '=', 'u')])
            template, = self.ProductTemplate.create([{
                'name': 'Test_Product',
                'type': 'goods',
                'default_uom': uom.id,
            }])

            product, = self.Product.create([{
                'template': template.id,
                'list_price': 5000,
                'cost_price': 4000,
            }])

            with self.assertRaises(Exception):
                product.template.list_price

            with self.assertRaises(Exception):
                product.template.cost_price

    def test0010_product_name(self):
        """
        Tests the searcher on the name field.
        """
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            uom, = self.Uom.search([], limit=1)
            template1, = self.ProductTemplate.create([{
                'name': 'ThisIsProduct',
                'type': 'goods',
                'list_price': Decimal('10'),
                'cost_price': Decimal('5'),
                'default_uom': uom.id,
            }])

            product1, = self.Product.create([{
                'template': template1.id,
                'code': 'SomeProductCode',
                'list_price': 5000,
                'cost_price': 4000,
            }])
            product2, = self.Product.create([{
                'template': template1.id,
                'code': 'SomeProductCode2',
                'variant_name': 'ADifferentName',
                'list_price': 5000,
                'cost_price': 4000,
            }])

            products = self.Product.search([
                ('name', '=', 'ThisIsProduct'),
            ])
            self.assertEqual(len(products), 2)

            products = self.Product.search([
                ('name', '=', 'ADifferentName'),
            ])
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0].id, product2.id)

            product1.variant_name = 'ChangedName'
            product1.save()

            products = self.Product.search([
                ('name', '=', 'ThisIsProduct'),
            ])
            self.assertEqual(len(products), 2)

# -*- coding: utf-8 -*-
"""
    test_sale

    Tests sale

    :copyright: (c) 2013-2015 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
import os
import sys
import unittest
DIR = os.path.abspath(os.path.normpath(
    os.path.join(
        __file__,
        '..', '..', '..', '..', '..', 'trytond'
    )
))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER, DB_NAME, CONTEXT
from test_base import TestBase, load_json
from trytond.transaction import Transaction


class TestSale(TestBase):
    """
    Tests import of sale order
    """

    def test_0010_import_sale_order(self):
        """
        Tests import of sale order using ebay data with ebay state as new
        """
        Sale = POOL.get('sale.sale')
        Party = POOL.get('party.party')
        Product = POOL.get('product.product')
        Listing = POOL.get('product.product.channel_listing')

        with Transaction().start(DB_NAME, USER, CONTEXT):
            self.setup_defaults()

            with Transaction().set_context({
                'current_channel': self.ebay_channel.id,
                'company': self.company
            }):

                orders = Sale.search([])
                self.assertEqual(len(orders), 0)

                order_data = load_json(
                    'orders', '283054010'
                )['OrderArray']['Order'][0]

                # We need to have SKU in all items of order_data
                order_data['TransactionArray']['Transaction'][0]['Item'].update(
                    {'SKU': 'test_sku1'}
                )
                order_data['TransactionArray']['Transaction'][1]['Item'].update(
                    {'SKU': 'test_sku2'}
                )

                Party.create_using_ebay_data(
                    load_json('users', 'testuser_ritu123')
                )

                ebay_data1 = load_json('products', '110162956809')
                ebay_data2 = load_json('products', '110162957156')

                # We need to have SKU in ebay_data
                ebay_data1['Item'].update({'SKU': 'test_sku1'})
                ebay_data2['Item'].update({'SKU': 'test_sku2'})

                # Create Product and Listing
                # Listing is required because if product is not found
                # then a new product is created from API request
                product1 = Product.create_using_ebay_data(
                    ebay_data1
                )
                Listing(
                    product=product1,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data1['Item']['ItemID']
                ).save()

                product2 = Product.create_using_ebay_data(
                    ebay_data2
                )
                Listing(
                    product=product2,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data2['Item']['ItemID']
                ).save()

                order1 = self.ebay_channel.import_order(order_data)

                self.assertEqual(order1.state, 'confirmed')

                orders = Sale.search([])
                self.assertEqual(len(orders), 1)

                # Item lines + shipping line should be equal to lines on tryton
                self.assertEqual(len(order1.lines), 3)

                order2 = self.ebay_channel.import_order(order_data)
                orders = Sale.search([])
                self.assertEqual(len(orders), 1)

                self.assertEqual(order1, order2)

    def test_0020_import_sale_order_with_exception(self):
        """
        Tests if exception is created for sale order when order total mismatch
        """
        Sale = POOL.get('sale.sale')
        Party = POOL.get('party.party')
        Product = POOL.get('product.product')
        ChannelException = POOL.get('channel.exception')
        Listing = POOL.get('product.product.channel_listing')

        with Transaction().start(DB_NAME, USER, CONTEXT):
            self.setup_defaults()

            with Transaction().set_context({
                'current_channel': self.ebay_channel.id,
                'company': self.company
            }):

                orders = Sale.search([])
                self.assertEqual(len(orders), 0)

                order_data = load_json(
                    'orders', '283054010'
                )['OrderArray']['Order'][0]

                # We need to have SKU in all items of order_data
                order_data['TransactionArray']['Transaction'][0]['Item'].update(
                    {'SKU': 'test_sku1'}
                )
                order_data['TransactionArray']['Transaction'][1]['Item'].update(
                    {'SKU': 'test_sku2'}
                )

                Party.create_using_ebay_data(
                    load_json('users', 'testuser_ritu123')
                )

                ebay_data1 = load_json('products', '110162956809')
                ebay_data2 = load_json('products', '110162957156')

                # We need to have SKU in ebay_data
                ebay_data1['Item'].update({'SKU': 'test_sku1'})
                ebay_data2['Item'].update({'SKU': 'test_sku2'})

                # Create Product and Listing
                # Listing is required because if product is not found
                # then a new product is created from API request
                product1 = Product.create_using_ebay_data(
                    ebay_data1
                )
                Listing(
                    product=product1,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data1['Item']['ItemID']
                ).save()

                product2 = Product.create_using_ebay_data(
                    ebay_data2
                )
                Listing(
                    product=product2,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data2['Item']['ItemID']
                ).save()

                self.assertEqual(order_data['Total']['value'], '4.0')

                self.assertFalse(ChannelException.search([]))

                # Lets Change order total to make it raise exception
                order_data['Total']['value'] = '8.5'

                order = self.ebay_channel.import_order(order_data)

                self.assertTrue(ChannelException.search([]))

                self.assertTrue(order.has_channel_exception)

                self.assertNotEqual(order.state, 'confirmed')

                orders = Sale.search([])
                self.assertEqual(len(orders), 1)

                # Item lines + shipping line should be equal to lines on tryton
                self.assertEqual(len(order.lines), 3)


def suite():
    """
    Test Suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestSale)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

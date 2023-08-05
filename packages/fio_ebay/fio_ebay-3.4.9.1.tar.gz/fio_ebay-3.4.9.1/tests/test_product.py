"""
    test_party

    Tests party

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


class TestProduct(TestBase):
    """
    Tests product
    """

    def test0010_import_product(self):
        """
        Test the import of simple product using eBay Data
        """
        Product = POOL.get('product.product')
        Listing = POOL.get('product.product.channel_listing')

        with Transaction().start(DB_NAME, USER, CONTEXT) as txn:
            self.setup_defaults()

            with txn.set_context({
                'current_channel': self.ebay_channel.id,
                'company': self.company,
            }):

                products_before_import = Product.search([], count=True)

                ebay_data = load_json('products', '110162956809')

                # We need to have SKU in ebay_data
                ebay_data['Item'].update({'SKU': 'test_sku1'})

                product = Product.create_using_ebay_data(
                    ebay_data
                )
                self.assertEqual(
                    product.template.name, 'Iphone'
                )

                products_after_import = Product.search([], count=True)
                self.assertTrue(products_after_import > products_before_import)

                # Create Listing for above product
                # Listing is required because if product is not found
                # then a new product is created from API request
                Listing(
                    product=product,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data['Item']['ItemID'],
                ).save()

                self.assertEqual(
                    product, self.ebay_channel.import_product(
                        ebay_data['Item']['SKU'],
                        product_data={'ItemID': ebay_data['Item']['ItemID']}
                    )
                )

    def test0020_create_product_duplicate(self):
        """
        Tests if items imported from ebay is duplicated as product in tryton
        """
        Product = POOL.get('product.product')
        Listing = POOL.get('product.product.channel_listing')

        with Transaction().start(DB_NAME, USER, CONTEXT) as txn:

            self.setup_defaults()

            with txn.set_context({
                'current_channel': self.ebay_channel.id,
                'company': self.company,
            }):
                self.assertEqual(Product.search([], count=True), 0)

                ebay_data = load_json('products', '110162956809')

                # We need to have SKU in ebay_data
                ebay_data['Item'].update({'SKU': 'test_sku2'})

                # Create product directly (assume its a new product)
                product = Product.create_using_ebay_data(
                    ebay_data
                )

                self.assert_(product)
                self.assertEqual(Product.search([], count=True), 1)

                # Listing is required because if product is not found
                # then a new product is created from API request
                Listing(
                    product=product,
                    channel=self.ebay_channel,
                    product_identifier=ebay_data['Item']['ItemID']
                ).save()

                # Create again
                product = self.ebay_channel.import_product(
                    ebay_data['Item']['SKU'],
                    product_data={'ItemID': ebay_data['Item']['ItemID']}
                )

                self.assertEqual(Product.search([], count=True), 1)


def suite():
    """
    Test Suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestProduct)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

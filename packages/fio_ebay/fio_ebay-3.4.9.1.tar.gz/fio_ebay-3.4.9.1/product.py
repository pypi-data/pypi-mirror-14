# -*- coding: UTF-8 -*-
'''
    product

    :copyright: (c) 2013-2015 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
'''
from itertools import groupby

from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from decimal import Decimal


__all__ = [
    'Product', 'ProductSaleChannelListing'
]
__metaclass__ = PoolMeta


class Product:
    "Product"

    __name__ = "product.product"

    @classmethod
    def extract_product_values_from_ebay_data(cls, product_data):
        """
        Extract product values from the ebay data, used for
        creation of product. This method can be overwritten by
        custom modules to store extra info to a product

        :param: product_data
        :returns: Dictionary of values
        """
        SaleChannel = Pool().get('sale.channel')

        ebay_channel = SaleChannel(Transaction().context['current_channel'])
        ebay_channel.validate_ebay_channel()
        return {
            'name': product_data['Item']['Title'],
            'default_uom': ebay_channel.default_uom.id,
            'salable': True,
            'sale_uom': ebay_channel.default_uom.id,
        }

    @classmethod
    def create_from(cls, channel, product_data):
        """
        Create product for channel
        """
        if channel.source != 'ebay':
            return super(Product, cls).create_from(channel, product_data)
        return cls.create_using_ebay_data(product_data)

    @classmethod
    def create_using_ebay_data(cls, product_data):
        """
        Create a new product with the `product_data` from ebay.

        :param product_data: Product Data from eBay
        :returns: Browse record of product created
        """
        Template = Pool().get('product.template')

        product_values = cls.extract_product_values_from_ebay_data(
            product_data
        )

        product_values.update({
            'products': [('create', [{
                'description': product_data['Item']['Description'],
                'list_price': Decimal(
                    product_data['Item']['BuyItNowPrice']['value'] or
                    product_data['Item']['StartPrice']['value']
                ),
                'cost_price':
                    Decimal(product_data['Item']['StartPrice']['value']),
                'code':
                    product_data['Item'].get('SKU', None) and
                    product_data['Item']['SKU'] or None,
            }])],
        })

        product_template, = Template.create([product_values])

        return product_template.products[0]


class ProductSaleChannelListing:
    "Product Sale Channel"
    __name__ = 'product.product.channel_listing'

    @classmethod
    def __setup__(cls):
        super(ProductSaleChannelListing, cls).__setup__()
        cls._error_messages.update({
            'inventory_update_fail': """
                Inventory Update failed for Product with SKU %s.
                ErrorCode: %s, ShortErrorMessage: %s
            """,
        })

    def export_inventory(self):
        """
        Export inventory of this listing to external channel
        """
        if self.channel.source != 'ebay':
            return super(ProductSaleChannelListing, self).export_inventory()

        self.export_bulk_inventory([self])

    @classmethod
    def export_bulk_inventory(cls, listings):
        """
        Bulk export inventory to Ebay
        """
        SaleChannelListing = Pool().get('product.product.channel_listing')

        if not listings:
            # Nothing to update
            return

        non_ebay_listings = cls.search([
            ('id', 'in', map(int, listings)),
            ('channel.source', '!=', 'ebay'),
        ])
        if non_ebay_listings:
            super(ProductSaleChannelListing, cls).export_bulk_inventory(
                non_ebay_listings
            )
        ebay_listings = filter(
            lambda l: l not in non_ebay_listings, listings
        )

        for channel, listings in groupby(ebay_listings, lambda l: l.channel):
            api = channel.get_ebay_trading_api()

            for listing in listings:
                product_data = {
                    'ItemID': listing.product_identifier,
                    'SKU': listing.product.code,
                    'Quantity': int(listing.quantity),
                }

                # TODO: Find a way to update inventory in bulk
                response = api.execute(
                    'ReviseInventoryStatus', {
                        'InventoryStatus': product_data
                    }
                ).dict()

                if response['InventoryStatus']['Quantity'] != int(listing.quantity):  # noqa
                    if response['Errors']['ErrorCode'] == '2191318':
                        # Products not found
                        listing, = SaleChannelListing.search([
                            ('product_identifier', '=',
                             product_data['ItemID']),
                            ('channel', '=', channel.id),
                        ])
                        listing.state = 'disabled'
                        listing.save()
                    else:
                        cls.raise_user_error(
                            'inventory_update_fail', (
                                product_data['SKU'],
                                response['Errors']['ErrorCode'],
                                response['Errors']['ShortMessage']
                            )
                        )

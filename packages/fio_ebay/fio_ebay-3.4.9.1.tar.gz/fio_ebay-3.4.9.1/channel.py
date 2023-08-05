# -*- coding: utf-8 -*-
"""
    channel.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
import dateutil.parser
from datetime import datetime

from ebaysdk.trading import Connection as trading
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, Button
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval


__all__ = [
    'SaleChannel', 'CheckEbayTokenStatusView', 'CheckEbayTokenStatus',
]
__metaclass__ = PoolMeta

EBAY_STATES = {
    'required': Eval('source') == 'ebay',
    'invisible': ~(Eval('source') == 'ebay')
}


class SaleChannel:
    "Sale Channel"
    __name__ = 'sale.channel'

    ebay_app_id = fields.Char(
        'eBay AppID', states=EBAY_STATES, depends=['source'],
        help="APP ID of the account - provided by eBay",
    )

    ebay_dev_id = fields.Char(
        'eBay DevID', help="Dev ID of account - provided by eBay",
        states=EBAY_STATES, depends=['source']
    )

    ebay_cert_id = fields.Char(
        'eBay CertID', help="Cert ID of account - provided by eBay",
        states=EBAY_STATES, depends=['source']
    )

    ebay_token = fields.Text(
        'eBay Token', states=EBAY_STATES, depends=['source'],
        help="Token for this user account - to be generated from eBay "
        "developer home. If it expirees, then a new one should be generated",
    )

    is_ebay_sandbox = fields.Boolean(
        'Is eBay sandbox ?',
        help="Select this if this account is a sandbox account",
        states={
            'invisible': ~(Eval('source') == 'ebay')
        }, depends=['source']
    )

    @classmethod
    def get_source(cls):
        """
        Get the source
        """
        sources = super(SaleChannel, cls).get_source()

        sources.append(('ebay', 'eBay'))

        return sources

    def get_last_order_import_time_required(self, name):
        """
        Change the getter to make last_order_import_time required for ebay
        """
        if self.source == 'ebay':
            return True

        return super(SaleChannel, self).get_last_order_import_time_required(
            name
        )

    @classmethod
    def __setup__(cls):
        """
        Setup the class before adding to pool
        """
        super(SaleChannel, cls).__setup__()

        cls._error_messages.update({
            "no_orders":
                'No new orders have been placed on eBay for this '
                'Channel after %s',
            "invalid_channel": "Current channel does not belong to eBay!",
            'same_ebay_credentials':
                'All the ebay credentials should be unique.'
        })
        cls._buttons.update({
            'check_ebay_token_status': {},
        })

    @classmethod
    def validate(cls, channels):
        """
        Validate sale channel
        """
        super(SaleChannel, cls).validate(channels)

        for channel in channels:
            channel.check_unique_app_dev_cert_token()

    def check_unique_app_dev_cert_token(self):
        """
        App ID, Dev ID, Cert ID and Token must be unique
        """
        if not all([
            self.ebay_app_id, self.ebay_dev_id,
            self.ebay_cert_id, self.ebay_token
        ]):
            return
        if self.search([
            ('ebay_app_id', '=', self.ebay_app_id),
            ('ebay_dev_id', '=', self.ebay_dev_id),
            ('ebay_cert_id', '=', self.ebay_cert_id),
            ('ebay_token', '=', self.ebay_token),
            ('id', '!=', self.id)
        ]):
            self.raise_user_error("same_ebay_credentials")

    def get_ebay_trading_api(self):
        """Create an instance of ebay trading api

        :return: ebay trading api instance
        """
        domain = 'api.sandbox.ebay.com' if \
            self.is_ebay_sandbox else 'api.ebay.com'
        return trading(
            appid=self.ebay_app_id,
            certid=self.ebay_cert_id,
            devid=self.ebay_dev_id,
            token=self.ebay_token,
            domain=domain,
            config_file=None,
        )

    @classmethod
    @ModelView.button_action('ebay.wizard_check_ebay_token_status')
    def check_ebay_token_status(cls, channels):
        """
        Check the status of token and display to user
        """
        pass

    def validate_ebay_channel(self):
        """
        Check if current channel belongs to ebay
        """
        if self.source != 'ebay':
            self.raise_user_error("invalid_channel")

    def import_orders(self):
        """
        Downstream implementation of channel.import_orders
        :return: List of active record of sale imported
        """
        if self.source != 'ebay':
            return super(SaleChannel, self).import_orders()

        self.validate_ebay_channel()

        sales = []
        api = self.get_ebay_trading_api()
        now = datetime.utcnow()

        last_import_time = self.last_order_import_time

        # Update current time for order update
        self.write([self], {'last_order_import_time': now})

        response = api.execute(
            'GetOrders', {
                'CreateTimeFrom': last_import_time,
                'CreateTimeTo': now
            }
        ).dict()
        if not response.get('OrderArray'):
            self.raise_user_error(
                'no_orders', (last_import_time, )
            )

        # Orders are returned as dictionary for single order and as
        # list for multiple orders.
        # Convert to list if dictionary is returned
        if isinstance(response['OrderArray']['Order'], dict):
            orders = [response['OrderArray']['Order']]
        else:
            orders = response['OrderArray']['Order']

        with Transaction().set_context({'current_channel': self.id}):
            for order_data in orders:
                sales.append(self.import_order(order_data))

        return sales

    def import_order(self, order_data):
        "Downstream implementation of channel.import_order from sale channel"
        if self.source != 'ebay':
            return super(SaleChannel, self).import_order(order_data)

        Sale = Pool().get('sale.sale')

        sales = Sale.search([
            ('channel_identifier', '=', order_data['OrderID']),
        ])
        if sales:
            return sales[0]

        return Sale.create_using_ebay_data(order_data)

    def import_product(self, sku, product_data=None):
        """
        Import specific product for this ebay channel
        Downstream implementation for channel.import_product
        """
        Product = Pool().get('product.product')
        Listing = Pool().get('product.product.channel_listing')

        if self.source != 'ebay':
            return super(SaleChannel, self).import_product(
                sku, product_data
            )

        # Check if there's a product with SKU (Ebay Custom Label)
        # The SKU on product may be different from that of listing
        # because SKU on a product on ebay is optional and is supplied
        # by user itself.
        existing_listings = Listing.search([
            ('product_identifier', '=', product_data['ItemID']),
            ('channel', '=', self),
        ])
        if existing_listings:
            return existing_listings[0].product

        products = Product.search([('code', '=', sku)])
        self.validate_ebay_channel()
        api = self.get_ebay_trading_api()
        full_product_data = None
        if not products:
            # If product is not found get the info from ebay and
            # delegate to create_from

            full_product_data = full_product_data or \
                api.execute(
                    'GetItem', {
                        'ItemID': product_data['ItemID'],
                        'DetailLevel': 'ReturnAll'
                    }
                ).dict()

            products = [Product.create_from(self, full_product_data)]

        product, = products
        listings = Listing.search([
            ('product', '=', product),
            ('channel', '=', self),
        ])
        if not listings:
            full_product_data = full_product_data or \
                api.execute(
                    'GetItem', {
                        'ItemID': product_data['ItemID'],
                        'DetailLevel': 'ReturnAll'
                    }
                ).dict()
            Listing(
                product=product,
                channel=self,
                product_identifier=full_product_data['Item']['ItemID'],
            ).save()

        return product


class CheckEbayTokenStatusView(ModelView):
    "Check Token Status View"
    __name__ = 'channel.ebay.check_token_status.view'

    status = fields.Char('Status', readonly=True)
    expiry_date = fields.DateTime('Expiry Date', readonly=True)


class CheckEbayTokenStatus(Wizard):
    """
    Check Token Status Wizard

    Check token status for the current ebay channel's token.
    """
    __name__ = 'channel.ebay.check_token_status'

    start = StateView(
        'channel.ebay.check_token_status.view',
        'ebay.check_ebay_token_status_view_form',
        [
            Button('OK', 'end', 'tryton-ok'),
        ]
    )

    def default_start(self, data):
        """
        Check the status of the token of the ebay channel

        :param data: Wizard data
        """
        SaleChannel = Pool().get('sale.channel')

        ebay_channel = SaleChannel(Transaction().context.get('active_id'))

        api = ebay_channel.get_ebay_trading_api()
        response = api.execute('GetTokenStatus').dict()

        return {
            'status': response['TokenStatus']['Status'],
            'expiry_date': dateutil.parser.parse(
                response['TokenStatus']['ExpirationTime']
            ),
        }

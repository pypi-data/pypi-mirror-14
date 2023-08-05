# -*- coding: utf-8 -*-
"""
    country

    Country

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
from trytond.pool import PoolMeta


__all__ = ['Subdivision']
__metaclass__ = PoolMeta


class Subdivision:
    "Subdivision"
    __name__ = 'country.subdivision'

    @classmethod
    def __setup__(cls):
        """
        Setup the class before adding to pool
        """
        super(Subdivision, cls).__setup__()
        cls._error_messages.update({
            'state_not_found': 'State %s does not exist in country %s.',
        })

    @classmethod
    def search_using_ebay_state(cls, value, country):
        """
        Searches for state with given ebay StateOrProvince value.

        :param value: Code or Name of state from ebay
        :param country: Active record of country
        :return: Active record of state if found else raises error
        """
        subdivisions = cls.search([
            ('country', '=', country.id),
            ('code', '=', country.code + '-' + value)
        ])

        if not subdivisions:
            subdivisions = cls.search([
                ('country', '=', country.id),
                ('name', 'ilike', value),
            ], limit=1)

        if not subdivisions:
            return cls.raise_user_error(
                "state_not_found", error_args=(value, country.name)
            )

        return subdivisions[0]

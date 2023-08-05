# -*- coding: utf-8 -*-
"""
    product.py

"""
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__metaclass__ = PoolMeta
__all__ = ['Template', 'Product']

STATES = {
    'readonly': ~Eval('active', True),
}
DEPENDS = ['active']


class Template:
    __name__ = "product.template"

    def get_prices(self, name):
        """Reached here! Just raise an exception to know what logic is using
        product template's prices?
        """
        raise Exception(
            "Product prices must be taken from product.product aka Variant"
        )

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        #: Use product.product list_price and cost_price.
        cls.list_price = fields.Function(
            fields.Numeric("List Price"), 'get_prices'
        )
        cls.cost_price = fields.Function(
            fields.Numeric("Cost Price"), 'get_prices'
        )


class Product:
    __name__ = "product.product"

    list_price = fields.Property(
        fields.Numeric(
            'List Price', digits=(16, 4), required=True,
            states=STATES, depends=DEPENDS
        )
    )
    cost_price = fields.Property(
        fields.Numeric(
            'Cost Price', digits=(16, 4), required=True,
            states=STATES, depends=DEPENDS
        )
    )

    name = fields.Function(
        fields.Char('Name'),
        getter='on_change_with_name', searcher='search_rec_name'
    )

    variant_name = fields.Char(
        'Variant Name', translate=True,
        select=True, states={
            'readonly': ~Eval('active', True),
        }, depends=['active']
    )

    @fields.depends('variant_name', 'template')
    def on_change_with_name(self, name=None):  # pragma: no cover
        """
        This method changes the name to `variant_name` if it is set, or else it
        returns the template name.
        """
        return self.variant_name or self.template.name

    @classmethod
    def search_rec_name(cls, name, clause):
        """
        Downstream implementation of `search_rec_name` which adds the
        variant_name field to the domain.
        """
        domain = super(Product, cls).search_rec_name(name, clause)
        domain.append(('variant_name', ) + tuple(clause[1:]))
        return domain

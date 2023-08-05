# -*- coding: utf-8 -*-
"""
    product_warehouse_location.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for more details.
"""
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta, Pool

__all__ = ['ProductWarehouseLocation', 'Product']
__metaclass__ = PoolMeta


class ProductWarehouseLocation(ModelSQL, ModelView):
    "Product Warehouse Location"
    __name__ = 'product.warehouse.location'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', required=True, select=True)
    product = fields.Many2One(
        'product.product', 'Product', required=True, select=True
    )
    warehouse = fields.Many2One(
        'stock.location', 'Warehouse',
        domain=[('type', '=', 'warehouse')],
        required=True, select=True
    )

    @classmethod
    def __setup__(cls):
        super(ProductWarehouseLocation, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def default_sequence():
        return 100


class Product:
    "Product"
    __name__ = 'product.product'

    warehouse_locations = fields.One2Many(
        'product.warehouse.location', 'product', 'Warehouse Locations'
    )

    def get_location_in(self, warehouse):
        """
        Return the location of the product in the given warehouse if one
        exits. If not None is returned
        """
        ProductWarehouseLocation = Pool().get('product.warehouse.location')

        locations = ProductWarehouseLocation.search([
            ('product', '=', self.id),
            ('warehouse', '=', warehouse.id),
        ])
        if locations:
            return locations[0].name

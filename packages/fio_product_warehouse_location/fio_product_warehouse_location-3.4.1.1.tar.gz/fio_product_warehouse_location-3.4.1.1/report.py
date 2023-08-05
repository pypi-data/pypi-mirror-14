# -*- coding: utf-8 -*-
from trytond.pool import Pool, PoolMeta


__all__ = ['ConsolidatedPickingList']
__metaclass__ = PoolMeta


class ConsolidatedPickingList:
    """
    Consolidated Picking List.
    """
    __name__ = 'report.consolidated_picking_list'

    @classmethod
    def group_key(cls, move):
        """
        Key function for grouping and sorting of
        moves
        """
        return (
            move.product.get_location_in(move.shipment.warehouse),
            move.product
        )

    @classmethod
    def get_location_repr_from(cls, key):
        """
        The location is a string or None
        """
        return key[0]

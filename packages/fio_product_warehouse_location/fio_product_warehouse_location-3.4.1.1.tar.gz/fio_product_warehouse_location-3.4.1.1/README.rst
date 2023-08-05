Product Warehouse Location Module
=================================

A lightweight implementation to keep track of where products are usually
in your warehouse. 

What this module is not:

  * Bin level inventory tracking (Stock module already does it).

When should I use this module ?
-------------------------------

We have worked with several small businesses where tracking down inventory
to the bin level is not practical. They neither have the resources to
spend on such discipline, nor does it give them a good return on
investment. However, they might still want to keep track of where their
products are kept within the warehouse. This module lets you do that,
without tracking the inventory at those levels.

If you are already using tryton's stock locations to keep track of
inventory at the bin level, you have no use of this module.

How does it work ?
------------------

The module adds a new list to the product screen where you can define
the locations where you should expect to find the products.

TODO
----

* Depend on stock report module and override them to show these locations.

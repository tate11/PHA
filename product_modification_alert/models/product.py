# -*- coding: utf-8 -*-

import itertools
import psycopg2

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat


class ProductTemplate(models.Model):
    """ Product Template inheritance to add an optional email.template to a
    product.template. When validating an invoice, an email will be send to the
    customer based on this template. The customer will receive an email for each
    product linked to an email template. """

    _inherit = ['product.template']

    def _get_default_category_id(self):
        if self._context.get('categ_id') or self._context.get('default_categ_id'):
            return self._context.get('categ_id') or self._context.get('default_categ_id')
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        if not category:
            category = self.env['product.category'].search([], limit=1)
        if category:
            return category.id
        else:
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)

    def _get_default_uom_id(self):
        return self.env["product.uom"].search([], limit=1, order='id').id

    name = fields.Char('Name', index=True, required=True, translate=True, track_visibility = 'onchange')
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying a product list')
    description = fields.Text(
        'Description', translate=True,
        help="A precise description of the Product, used only for internal information purposes.", track_visibility = 'onchange')
    description_purchase = fields.Text(
        'Purchase Description', translate=True,
        help="A description of the Product that you want to communicate to your vendors. "
             "This description will be copied to every Purchase Order, Receipt and Vendor Bill/Credit Note.", track_visibility = 'onchange')
    description_sale = fields.Text(
        'Sale Description', translate=True,
        help="A description of the Product that you want to communicate to your customers. "
             "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note", track_visibility = 'onchange')
    type = fields.Selection([
        ('consu', _('Consumable')),
        ('service', _('Service'))], string='Product Type', default='consu', required=True,
        help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
             'A consumable product, on the other hand, is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A digital content is a non-material product you sell online. The files attached to the products are the one that are sold on '
             'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.', track_visibility = 'onchange')
    rental = fields.Boolean('Can be Rent')
    categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, default=_get_default_category_id,
        required=True, help="Select category for the current product", track_visibility = 'onchange')

    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id', track_visibility = 'onchange')

    # price fields
    price = fields.Float(
        'Price', compute='_compute_template_price', inverse='_set_template_price',
        digits=dp.get_precision('Product Price'), track_visibility = 'onchange')
    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits=dp.get_precision('Product Price'),
        help="Base price to compute the customer price. Sometimes called the catalog price.", track_visibility = 'onchange')
    lst_price = fields.Float(
        'Public Price', related='list_price',
        digits=dp.get_precision('Product Price'), track_visibility = 'onchange')
    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits=dp.get_precision('Product Price'), groups="base.group_user",
        help = "Cost used for stock valuation in standard price and as a first price to set in average/fifo. "
               "Also used as a base price for pricelists. "
               "Expressed in the default unit of measure of the product. ", track_visibility = 'onchange')


    #
    # name = fields.Char('Name', track_visibility = 'onchange')
    # sale_ok = fields.Boolean(
    #     'Can be Sold', default=True,
    #     help="Specify if the product can be selected in a sales order line.", track_visibility = 'onchange')
    # purchase_ok = fields.Boolean('Can be Purchased', default=True)
    # pricelist_id = fields.Many2one(
    #     'product.pricelist', 'Pricelist', store=False,
    #     help='Technical field. Used for searching on pricelists, not stored in database.', track_visibility = 'onchange')

    # , track_visibility = 'onchange'
    # list_price = fields.Float(
    #     'Sales Price', default=1.0,
    #     digits=dp.get_precision('Product Price'),
    #     help="Base price to compute the customer price. Sometimes called the catalog price.")
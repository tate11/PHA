# -*- coding: utf-8 -*-

import itertools
import psycopg2

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat


class ResPartner(models.Model):
    _inherit = ['res.partner']

    suppliers_ids = fields.One2many('product.supplierinfo', 'name', string='prix fournisseurs')


class ProductSupplierinfor(models.Model):
    _inherit = ['product.supplierinfo']

    max_qty= fields.Float(
        'Maximal Quantity', default=0.0, required=True,)





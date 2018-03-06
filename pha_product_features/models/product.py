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


    description = fields.Text(string='Description')
    material = fields.Char(string='Matière')
    dimension = fields.Char(string='Dimension')
    diameter = fields.Char(string='Diamètre')

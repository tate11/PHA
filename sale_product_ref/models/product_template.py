# -*- coding: utf-8 -*-
from openerp import models, fields
import logging
class sale_product_ref(models.Model):
    _name= "sale.product.ref"
    _rec_name = "label"

    sequence = fields.Integer('sequence',
                              help="Sequence for the handle.")

    ref =fields.Char(string="reference",
                     required= True)

    label =fields.Char(string="label",
                       required= True)

    price =fields.Float(string="price",
                        required= True,)


    _sql_constraints = [
        ('ref_unique',
         'unique(ref)',
         'Choose another value Reference has to be unique!')
    ]


    def _get_default_price(self):

        logging.warning("context"+self._context)

        return 10

    _defaults = {
        'price': _get_default_price,
    }


class product_template(models.Model):
    _inherit = "product.template"

    product_ref_list = fields.Many2many("sale.product.ref",
                                       string="product refs")
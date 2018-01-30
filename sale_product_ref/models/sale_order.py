# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging


class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    product_ref_list = fields.One2many(comodel="sale.product.ref",
                                       related="product_id.product_ref_list")

    sale_product_ref = fields.Many2one("sale.product.ref", required= True)

    @api.onchange('product_id')
    def _onchange_product(self):
        pass
        domain_ids = []
        for p_r in self.product_ref_list:
            domain_ids.append(p_r.id)

        domain =  [('id','in',domain_ids)]
        return {
            'domain' : {
                'sale_product_ref': domain
            }
        }

    @api.onchange('sale_product_ref')
    def onchange_prd_ref(self):
        self.price_unit = self.sale_product_ref.price
        self.name=  "["+str(self.sale_product_ref.label)+"] "+str(self.name).split('] ')[-1]
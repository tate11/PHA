# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

logger = logging.getLogger()
logger.propagate = False


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_product_ids = fields.Many2many('product.product')

    @api.onchange('partner_id')
    def onchange_partner_product(self):
        seller_ids = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id)])

        product_ids = []
        for s in seller_ids:
            logging.warning('onchange seller_ids' + str(s.product_tmpl_id.name))
            if not s.product_id.id:
                product_ids.append(s.product_tmpl_id.product_variant_id.id)
            else:
                product_ids.append(s.product_id.id)

        self.partner_product_ids = [(6, 0, product_ids)]

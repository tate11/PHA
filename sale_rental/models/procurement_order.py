# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    @api.model
    def create(self, vals):
        if 'rental_product_qty' in vals:
            vals['product_qty'] = vals['rental_product_qty']
            vals.pop('rental_product_qty')
        return super(ProcurementGroup, self).create(vals)

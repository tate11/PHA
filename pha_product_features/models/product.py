# -*- coding: utf-8 -*-

import itertools
import psycopg2

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _


class ProductMateriales(models.Model):
    _name='product.materiales'

    name =fields.Char(string='Matière')


class ProductTemplate(models.Model):
    """ Product Template inheritance to add an optional features to a
    product.template. . """

    _inherit = ['product.template']
    description =fields.Text(string='Description')
    # material =fields.Many2one('product.materiales',string='Matière')
    dimension = fields.Char(string='Dimension')
    diameter = fields.Char(string='Diamètre')

    material_id = fields.Many2one('product.materiales',string='Matière')

    # @api.multi
    # def _get_name_material(self):
    #     for obj in self:
    #         obj.name = '%s ' % (obj.material_id.name)
    #
    # material = fields.Char(string='Matière', compute='_get_name_material')

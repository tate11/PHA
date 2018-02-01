# -*- coding: utf-8 -*-
from openerp import models, fields
import logging


class product_template(models.Model):
    _inherit = "product.template"

    travee = fields.Char(string ="Travée")
    etagere = fields.Char(string = "Etagére")
    colonne = fields.Char(string = "colonne")
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64, csv
from io import BytesIO
import logging
from odoo.tools import pycompat


class InventoryImportLine(models.TransientModel):
    _name = "stock.inventory.import.line"

    travee = fields.Char(string="Travée")
    etagere = fields.Char(string="Etagére")
    colonne = fields.Char(string="colonne")
    name = fields.Char(string = "name")
    default_code = fields.Char('Internal Reference', index=True)






    state = fields.Selection(selection=[('valid', 'valid'),
                                        ('not_valid', 'Not valid'),
                                        ('product_not_spec', 'Produit non spécifié'),
                                       ],
                            default='valid'
                             )
            
class InventoryImport(models.TransientModel):
    _name = "stock.inventory.import"

    data = fields.Binary('Fichier',
                         required=True,
                         default=lambda self: self._context.get('data'))

    name = fields.Char('Filename')
    delimeter = fields.Char('Delimeter',
                            default=';',
                            help='Default delimeter is ";"')

    lineterminator = fields.Char('Line terminator',
                            default='\n',
                            help='Default delimeter is "\n"')

    state = fields.Selection(selection=[('draft', 'Brouillon'),
                                        ('validated', 'Validation'),
                                        ('imported', 'Importation')],
                             default=lambda self: self._context.get('state','draft')
                             )

    reader_info = []

    stock_inventory_ids = fields.Many2many('stock.inventory.import.line',
                                                default=lambda self: self._context.get('stock_inventory_ids'))
    @api.multi
    def _get_stock_inventory_from_csv(self):

        stock_inventory_items = []
        list = enumerate(self.reader_info)
        logging.error('reader_info '+str(self.reader_info))
        for i, csv_line in list:
            logging.info("line %s => %s line", i, csv_line)
            if i > 0:

                product_id = self.env['product.product'].search([('default_code', '=', csv_line[0])])

                inv_item['name'] = csv_line[0]
                inv_item = {}

                if product_id:
                    inv_item['state'] = 'valid'


                else:
                    inv_item['state'] ='product_not_spec'



                stock_inventory_items.append((0,0,inv_item))

        return stock_inventory_items


    @api.multi
    def validate(self):

        if not self.data:
            raise exceptions.Warning(_("You need to select a file!"))

        csv_data = base64.b64decode(self.data)
        csv_data = BytesIO(csv_data.decode('utf-8').encode('utf-8'))
        csv_iterator = pycompat.csv_reader(csv_data,delimiter=";")

        logging.info("csv_iterator" + str(csv_iterator))

        try:
            self.reader_info=[]
            self.reader_info.extend(csv_iterator)
            csv_data.close()
            # self.stock_production_lot_ids = self._get_stock_prd_lot_from_csv()
            self.state= 'validated'
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))




        return {
            'name': ('Assignment Sub'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.inventory.import',
            'view_id': False,
            'context': {'data':self.data,
                        'state': self.state,
                        'stock_inventory_ids': self._get_stock_inventory_from_csv()},
            'type': 'ir.actions.act_window',
            'target':'new'
        }

    @api.multi
    def import_inventory(self):

        unvalid_items = []
        for line in self.stock_inventory_ids:

            logging.warning('line.state => ' + str(line.state))

            inv_item = {'product_id': line.product_id.id,
                        'name': line.name,
                        }
            if line.state == 'valid':


                line_existed = self._check_if_exists(inv_item['product_id'], inv_item['name'])
                logging.warning('line.product_id => '+str(line.product_id))
                if not line_existed:
                    self.env['stock.production.line'].create(inv_item)
                    inv_item['state'] = 'product_imported'
                else:
                    inv_item['state'] = 'lot_exist'
            else :
                inv_item['state'] = line.state
            unvalid_items.append((0,0,inv_item))


        self.state = 'imported'
        return {
            'name': ('Assignment Sub'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.production.lot.import',
            'view_id': False,
            'context': {'data': self.data,
                        'stock_production_lot_ids': unvalid_items,
                        'state': self.state},
            'type': 'ir.actions.act_window',
            'target': 'new'
        }



    def _check_if_exists(self, product_id):

        product_id = self.env['product.product'].search(
            [('id', '=', product_id)])

        if len(product_id) > 0:
            return product_id
        else:
            return False

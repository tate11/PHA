# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Auguria (<http://www.auguria.net>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.exceptions import Warning
import logging
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
from lxml import etree

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class product_product(osv.osv):
    _inherit = "product.product"
    
    #AMA : ajout calculette
    _columns = {
          # 'product_supplier_id': fields.one2many('product.supplierinfo', 'product_tmpl_id', 'Supplier'),
          # 'pricelist_ids': fields.one2many('pricelist.partnerinfo', 'suppinfo_id', 'Supplier Pricelist', copy=True),
            'prix_achat_ht': fields.float('Prix achat HT', digits_compute=dp.get_precision('Product Price')),
            'frais_transport': fields.float('Frais transport HT', digits_compute=dp.get_precision('Product Price')),
            'prix_achat_ttc_hide': fields.float('Cout revient  TTC', digits_compute=dp.get_precision('Product Price'), store=True),
            'prix_achat_ttc':fields.related('prix_achat_ttc_hide', string="Cout revient  TTC", help="(PA HT + frais transport) + TVA"),
            'taux_tva': fields.float('Taux tva', digits_compute=dp.get_precision('Product Price')),
            'cout_manutention': fields.float('Manutention Price', digits_compute=dp.get_precision('Manutention Price')),
            'prix_vente_ht': fields.float('Prix vente HT', digits_compute=dp.get_precision('Product Price')),
            'prix_vente_ttc': fields.float('Prix vente TTC', digits_compute=dp.get_precision('Product Price')),
            'taux_marge': fields.float('Taux de marge', digits_compute=dp.get_precision('Product Price'),
                            help="Taux de marge = (( PV HT - PA HT)) / PA HT ) * 100"),

            'montant_marge_hide': fields.float('Marge brute', digits_compute=dp.get_precision('Product Price'),),
            'montant_audit': fields.float('Cout Audit', digits_compute=dp.get_precision('Audit Price'), ),
            'montant_marge':fields.related('montant_marge_hide', string="Marge brute sur PV", help="Marge brute = PV HT - PA HT"),
            'coef_multi_hide': fields.float(string='Coef. multiplicateur', digits_compute=dp.get_precision('Product Price')),
            'coef_multi' : fields.related('coef_multi_hide', string="Coefficient multiplicateur", help="PV TTC / COUT REVIENT HT"),
            'taux_marque_hide': fields.float('Taux de marque', digits_compute=dp.get_precision('Product Price')),
            'taux_marque' : fields.related("taux_marque_hide", string="Taux de marque", help="Taux de marque = (( PV HT - PA HT)) / PV HT ) * 100"),
            'type_tva2': fields.selection((('n', 'TVA Classique'), ('c', 'TVA sur marge')), 'Type de TVA', default='n')
    }
    
    _defaults = {
        'taux_tva': 20.0,
        'taux_marge':0.0,
        'montant_marge':0.0,
        'taux_marque':0.0,
        #'prix_vente_ht' : lambda self, cr, uid, context: self.pool.get('product.template').browse(cr, uid, uid, context=context).list_price,
    }


    
    def prix_achat_ht_change(self, cr, uid, ids, prix_achat_ht, frais_transport, prix_vente_ht, taux_tva,  context=None):
        if not prix_achat_ht:
            return {}
        result = {}
        coef_tva = 1 + (taux_tva / 100)
        prix_achat_trans = prix_achat_ht + frais_transport
        
        result['prix_achat_ttc_hide'] = prix_achat_trans * coef_tva
        result['prix_achat_ttc'] = result['prix_achat_ttc_hide']
        
        montant_marge = prix_vente_ht - prix_achat_trans
        result['montant_marge_hide'] = montant_marge
        result['montant_marge'] = result['montant_marge_hide']
        
        if montant_marge > 0:
            result['taux_marge'] = (montant_marge / prix_achat_trans) * 100
            result['taux_marque_hide'] = (montant_marge / prix_vente_ht) * 100
            result['taux_marque'] = result['taux_marque_hide']
            
            prix_vente_ttc = prix_vente_ht * coef_tva
            result['coef_multi_hide'] = prix_vente_ttc / prix_achat_trans
            result['coef_multi'] = result['coef_multi_hide']
        else:
            result['taux_marge'] = 0
            result['coef_multi_hide'] = 0
            result['coef_multi'] = result['coef_multi_hide']
            result['taux_marque_hide'] = 0
            result['taux_marque'] = result['taux_marque_hide']
        
        return {'value': result}
    
    def tva_change(self, cr, uid, ids, prix_achat_ht,frais_transport, prix_vente_ht, taux_tva, montant_marge,  context=None):
        result = {}
        coef_tva = 1 + (taux_tva / 100)
        prix_achat_trans = prix_achat_ht + frais_transport
        prix_vente_ttc = prix_vente_ht * coef_tva
        
        result['prix_achat_ttc_hide'] = prix_achat_trans * coef_tva
        result['prix_achat_ttc'] = result['prix_achat_ttc_hide']
        
        result['prix_vente_ttc'] = prix_vente_ttc
        
        if montant_marge > 0:
            result['coef_multi_hide'] = prix_vente_ttc / prix_achat_trans
            result['coef_multi'] = result['coef_multi_hide']
        else:
            result['coef_multi_hide'] = 0
            result['coef_multi'] = result['coef_multi_hide']
        
        return {'value': result}
    
    def prix_vente_ht_change(self, cr, uid, ids, prix_vente_ht, prix_achat_ht, frais_transport, taux_tva, context=None):
        result = {}
        coef_tva = 1 + (taux_tva / 100)
        prix_achat_trans = prix_achat_ht + frais_transport
        
        prix_vente_ttc = prix_vente_ht * coef_tva
        result['prix_vente_ttc'] = prix_vente_ttc
        montant_marge = prix_vente_ht - prix_achat_trans
        
        result['montant_marge_hide'] = montant_marge
        result['montant_marge'] = result['montant_marge_hide']
        
        if montant_marge > 0:
            result['taux_marge'] = (montant_marge / prix_achat_trans) *100
            result['taux_marque_hide'] = (montant_marge / prix_vente_ht) * 100
            result['taux_marque'] = result['taux_marque_hide']
            result['coef_multi_hide'] = prix_vente_ttc / prix_achat_trans
            result['coef_multi'] = result['coef_multi_hide']
        else:
            result['taux_marge'] = 0
            result['coef_multi_hide'] = 0
            result['coef_multi'] = result['coef_multi_hide']
            result['taux_marque_hide'] = 0
            result['taux_marque'] = result['taux_marque_hide']
            
        return {'value': result}
    
    def prix_vente_ttc_change(self, cr, uid, ids, prix_vente_ttc, prix_achat_ht, frais_transport, taux_tva, context=None):
        result = {}
        coef_tva = 1 + (taux_tva / 100)
        prix_achat_trans = prix_achat_ht + frais_transport
        
        prix_vente_ht = prix_vente_ttc / coef_tva
        result['prix_vente_ht'] = prix_vente_ht
        montant_marge = prix_vente_ht - prix_achat_trans
        result['montant_marge_hide'] = montant_marge
        result['montant_marge'] = result['montant_marge_hide']
        
        if montant_marge > 0:
            result['taux_marge'] = (montant_marge / prix_achat_trans) *100
            result['taux_marque_hide'] = (montant_marge / prix_vente_ht) * 100
            result['taux_marque'] = result['taux_marque_hide']
            result['coef_multi_hide'] = prix_vente_ttc / prix_achat_trans
            result['coef_multi'] = result['coef_multi_hide']
        else:
            result['taux_marge'] = 0
            result['coef_multi_hide'] = 0
            result['coef_multi'] = result['coef_multi_hide']
            result['taux_marque_hide'] = 0
            result['taux_marque'] = result['taux_marque_hide']
            
        return {'value': result}
    
    def taux_marge_change(self, cr, uid, ids, prix_achat_ht, frais_transport, taux_marge, taux_tva, context=None):
        result = {}
        coef_tva = 1 + (taux_tva / 100)
        coef_marge = 1 + (taux_marge / 100)
        prix_achat_trans = prix_achat_ht + frais_transport
        
        prix_vente_ht = prix_achat_trans * coef_marge
        result['prix_vente_ht'] = prix_vente_ht
        prix_vente_ttc = prix_vente_ht * coef_tva
        result['prix_vente_ttc'] = prix_vente_ttc
        
        montant_marge = prix_vente_ht - prix_achat_trans
        result['montant_marge_hide'] = montant_marge 
        result['montant_marge'] = result['montant_marge_hide']
        
        if montant_marge > 0:
            result['coef_multi_hide'] = prix_vente_ttc / prix_achat_trans
            result['coef_multi'] = result['coef_multi_hide']
            result['taux_marque_hide'] = (montant_marge / prix_vente_ht) * 100
            result['taux_marque'] = result['taux_marque_hide']
        else:
            result['coef_multi_hide'] = 0
            result['coef_multi'] = result['coef_multi_hide']
            result['taux_marque_hide'] = 0
            result['taux_marque'] = result['taux_marque_hide']
        
        return {'value': result}
    
#class product_supplierinfo(osv.osv):
#   _name = "product.supplierinfo"
#   _inherit = "product.supplierinfo"
#      
#   def name_get(self, cr, uid, ids, context=None):
#       if not ids:
#           return []
#       if isinstance(ids, (int, long)):
#                   ids = [ids]
#       reads = self.read(cr, uid, ids, ['name'], context=context)
#       res = []
#       for record in reads:
#           name = record['name']
#           res.append((record['id'], name))
#       return res
    
    
#class product_product(osv.osv):
#    _inherit = "product.product"

    #le champs reference interne devient obligatoire
#    _columns = {
 #       'default_code' : fields.char('Internal Reference', select=True, required=True),
  #  }


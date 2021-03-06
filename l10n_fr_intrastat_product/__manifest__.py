# -*- encoding: utf-8 -*-
##############################################################################
#
#    Report intrastat product module for OpenERP
#    Copyright (C) 2010-2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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


{
    'name': 'France Intrastat Product agilorg',
    'version': '1.0',
    'category': 'Localisation/Report Intrastat',
    'license': 'AGPL-3',
    'summary': 'Module for Intrastat product reporting (DEB) for France',
    'description': """This module adds support for the "Déclaration d'Echange de Biens" (DEB).

More information about the DEB is available on this official web page : http://www.douane.gouv.fr/page.asp?id=322

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['intrastat_product', 'sale_stock', 'purchase', 'l10n_fr_siret'],
    'data': [
        'security/intrastat_product_security.xml',
        'security/ir.model.access.csv',
        'data/intrastat_product_reminder.xml',
        'data/intrastat_type_data.xml',
        'views/intrastat_product_view.xml',
        'views/intrastat_type_view.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/stock_view.xml',
        'views/invoice_view.xml',
    ],
    'demo': ['demo/intrastat_demo.xml'],
    'installable': True,
    'application': True,
}

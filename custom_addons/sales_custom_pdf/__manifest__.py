# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "sales_custom_pdf",
    'version': '0.1',
    'summary': 'Overrides pdf for sales module',
    'description': "Overrides pdf sales module this is a test from custom development tutorial",
    'website': 'https://www.orion10x.net/',
    'depends': ['base'],
    'data': [
        'report/sales_report_inherited.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "pos_receipt",
    'version': '0.1',
    'summary': 'Overrides the default POS receipt layout',
    'description': "Overrides the default POS receipt layout",
    'website': 'https://www.orion10x.net/',
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_receipt/static/src/js/**/*',
            'pos_receipt/static/src/xml/**/*'
        ]
    },
    'installable': True,
    'auto_install': True,
}
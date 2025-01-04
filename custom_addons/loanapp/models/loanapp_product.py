
from odoo import fields, models

class LoanAppProduct(models.Model):

    _name = 'loanapp_product'
    _description = 'Loan App Product'

    name = fields.Char(string='Product Name', required=True)
    short_name = fields.Char(string='Short Name', required=True)
    default_amount = fields.Float(string='Default Amount', required=True, default=0)
    max_amount = fields.Float(string='Max Amount', required=True, default=0)
    min_amount = fields.Float(string='Min Amount', required=True, default=0)

    default_interest = fields.Float(string='Default Interest', required=True, default=0)
    min_interest = fields.Float(string='Min Interest', required=True, default=0)
    max_interest = fields.Float(string='Max Interest', required=True, default=0)

    _sql_constraints = [
            ('check_min_interest', 'CHECK(min_interest >= 0 AND min_interest <= max_interest)',
             'The percentage of minimum interest should be greater than 0 and less than max_interest'),
        ('check_max_interest', 'CHECK(max_interest >= 0 AND max_interest >= min_interest)',
         'The percentage of maximum interest should be greater than 0 and greater than min_interest'),

        ('check_min_max_interest', 'CHECK(max_interest >= min_interest)',
         'The minimum interest should be less or equal to maximum interest.'),

        ('check_default_interest', 'CHECK(default_interest >= min_interest AND default_interest <= max_interest)',
         'The percentage of default interest  should be between range of min and max values.'),


        ('unique_product_name', 'UNIQUE(name)', 'product name must be unique'),
        ('unique_short_name', 'UNIQUE(short_name)', 'product short name must be unique')
    ]


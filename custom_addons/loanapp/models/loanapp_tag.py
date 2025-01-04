from odoo import fields, models


class LoanAppTag(models.Model):

    _name = 'loanapp_tag'
    _description = 'Loan App Tag'

    name = fields.Char(string='Tag', required=True);
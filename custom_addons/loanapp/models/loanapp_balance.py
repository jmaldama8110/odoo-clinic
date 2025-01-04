from odoo import models,fields

class LoanAppBalance(models.Model):

    _name = 'loanapp_balance'
    _description = 'Loan App Balance'

    loanapp_application_id = fields.Many2one('loanapp_application')
    current_balance = fields.Float(string='Current Balance')
    accrued_interest = fields.Float(string='Accrued Interest')
    accrued_tax = fields.Float(string='Accrued Tax')
    paid_principal = fields.Float(string='Paid Principal')
    paid_interest = fields.Float(string='Paid Interest')
    paid_tax = fields.Float(string='Paid Tax')
    paid_total = fields.Float(string='Paid Total')

    status = fields.Selection([ ('a','OnTime'),('b','Upfront'),('c','Past-due')])

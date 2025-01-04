from odoo import models,fields

class LoanAppRepayPlan(models.Model):

        _name = 'loanapp_repayplan'
        _description = 'Loan Application Repay Plan'

        loanapp_application_id = fields.Many2one('loanapp_application', string='Loan Application Application')
        payment_number = fields.Integer(string='Payment Number',required=True)
        date_start = fields.Date(string='Start Date', required=True)
        date_end = fields.Date(string='End Date', required=True)
        repay_amount = fields.Float(string='Amount',required=True);
        interest_amount = fields.Float(string='Interest Amount',required=True)
        principal_amount = fields.Float(string='Principal Amount', required=True)
        tax_amount = fields.Float(string='Tax Amount',required=True)
        loan_balance = fields.Float(string='Loan Balance',required=True)


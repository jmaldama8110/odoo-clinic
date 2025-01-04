from odoo import fields,models

class LoanAppGuarantor(models.Model):
    _name = 'loanapp_guarantor'
    _description = 'Loan App Guarantor'

    contact_id = fields.Many2one('res.partner', string='Contact ID',required=True)
    loanapp_application_id = fields.Many2one('loanapp_application', string='Loan App Application',required=True)
    phone = fields.Char(string='Phone', required=True)
    date_of_verification = fields.Date(string='Date of Verification', required=True)
    status = fields.Selection( [('d','Draft'),('a','Accepted'),('x','Refused')] )

    def action_confirm(self):
            for record in self:
                self.status = 'a'


    def action_cancel(self):
        for record in self:
            self.status = 'x'
        return True



from odoo import api,models,fields
from odoo.exceptions import ValidationError
from odoo.tools import float_compare
import math

#ME QUEDE EN QUE TENGO QUE BUSCAR
#COMO UN BOTON PUEDE ABRIR UN DIALOGO PARA
#CREAR UN DESEMBOLSO, Y UN REGISTRO

class LoanAppApplication(models.Model):

    _name = 'loanapp_application'
    _description = 'Loan Application model'

    name = fields.Char(compute='_client_name')
    @api.depends('contact_id.name')
    def _client_name(self):
        for record in self:
            record.name = "Loan for %s" % record.contact_id.name

    # when selection changes, it sets default loan amount based on product definition
    product_id = fields.Many2one('loanapp_product', string='Product', required=True)
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.apply_amount = self.product_id.default_amount
    # short_name is set from loanapp_product model
    short_name = fields.Char(compute='_product_short_name')
    def _product_short_name(self):
        for record in self:
            record.short_name = record.product_id.short_name


    contact_id = fields.Many2one("res.partner", string="Contact",required=True)
    officer_id = fields.Many2one('res.users', string='Officer', index=True, tracking=True, default=lambda self: self.env.user)
    currency_id = fields.Many2one('res.currency', string='Currency', default=33)

    apply_amount = fields.Float(string='Apply Amount')
    @api.constrains('apply_amount')
    def _check_apply_amount(self):
        if self.apply_amount < 0:
            raise ValidationError('Apply amount should be greater than zero')
        if float_compare(self.apply_amount, self.product_id.min_amount,0,1) < 0:
            raise ValidationError('Apply amount should be greater than product minimum amount')
        if float_compare(self.apply_amount, self.product_id.max_amount,0,1) > 0:
            raise ValidationError('Apply amount should be below than product maximum amount')

    term = fields.Integer( string='Term', required=True, default=6)
    term_type = fields.Selection([ ('w','Weeks'),('m','Months'),('q','Bimonthly')], default='m', string='Term Type',required=True)
    frequency = fields.Selection([ ('wl','Weekly'),('ml','Monthly')], default='wl', string='Frequency',required=True);
    status = fields.Selection( [('a','Draft'),('b','Accepted'),('c','Approved'),('d','Disbursed'),('x','Canceled'),('r','Refused')],required=True, default='a')
    date_apply = fields.Date(string='Application Date');
    @api.constrains('date_apply')
    def _check_date_apply(self):
        for record in self:
            if record.date_apply > fields.Date.today():
                raise ValidationError('Application date should not be in the future')

    date_disbursement = fields.Date(string='Disbursement Date');
    @api.constrains('date_disbursement')
    def _check_date_disbursement(self):
        for record in self:
            if record.date_disbursement < fields.Date.today():
                raise ValidationError('Disbursement date should not be in the past')
    date_plan_start = fields.Date(string='Start Date');
    def _check_date_plan_start(self):
        for record in self:
            if record.date_plan_start < fields.Date.today():
                raise ValidationError('Date start plan should not be in the past')
            if record.date_plan_start < record.date_disbursement:
                raise ValidationError('Date start plan should can not be earlier than disbursement date')

    date_plan_end = fields.Date(string='End Date');

    installment_capital = fields.Float(string='Installment Capital')
    installment_interest = fields.Float(string='Installment Interest')
    installment_tax = fields.Float(string='Installment Tax')
    installment_amount = fields.Float(compute="_installment_amount",inverse='_inverse_installment_amount',string='Installment Amount',default=0, required=True)
    @api.depends('apply_amount','term','term_type','frequency','interest_rate')
    def _installment_amount(self):
        for record in self:
            if record.term > 0:
                record.installment_amount =  calc_installment(record.apply_amount,record.interest_rate,record.term, record.term_type)

    #ASEGURAR QUE EL USUARIO GENERE NUEVAMENTE EL PLAN DE PAGOS
    #POR MEDIO DE VALIDACION DEL TOTAL EN LOANAPP_REPAYPLAN VS TOTAL DEL APPLY AMOUNT
    #EL NUMERO DE CUOTAS PAYMENT NUMBER DEBE SER IGUAL QUE EL TERM
    #Y EL IMPORTE FIJO DEBE SER IGUAL QUE LAS CUOTAS DEL PLAN

    #TUTORIAL CONTINUA CON ADD THE SPRINKLES
    #INHERITANCE
    #INTERACT WITH OTHER MODULES
    #QWEB
    #FINAL WORD

    def _inverse_installment_amount(self):
        for record in self:
            if record.apply_amount > 0:
                if record.installment_amount > 0:
                    record.term = calc_term(record.apply_amount,record.interest_rate,record.installment_amount,record.term_type)

    interest_rate = fields.Float(string='Interest Rate', required=True,default=12.0);
    installment_type = fields.Selection([ ('f','Fixed'),('d','Diminishing')],default='f',string='Installment Type',required=True);

    loan_purpose = fields.Selection([ ('1','Working Capital'),('2','Asset Acquisition'),('3','Bank Acquisition'),('3','Other')], default='1',string='Purpose');
    main_occupation = fields.Selection([ ('1','Working Capital'),('2','Asset Acquisition'),('3','Bank Acquisition'),('3','Other')], default='1',string='Occupation');
    customer_profession = fields.Selection([ ('1','Engineer'),('2','Carpenter'),('3','Drive'),('3','Business Person')], default='1',string='Profession');
    customer_economic_activity = fields.Selection([ ('1','Working Capital'),('2','Asset Acquisition'),('3','Bank Acquisition'),('3','Other')], default='1',string='Economic Activity');

    income_salary = fields.Float(string='Income Salary', required=True, default=0)
    income_remittances = fields.Float(string='Income Remittance', required=True, default=0)
    income_spouse = fields.Float(string='Income Spouse', required=True, default=0)
    income_others = fields.Float(string='Income Others', required=True,default=0)

    total_income = fields.Float(compute='_total_income', string='Total Income')
    @api.depends('income_salary','income_remittances','income_spouse','income_others')
    def _total_income(self):
        for record in self:
            record.total_income = record.income_salary + record.income_remittances + record.income_spouse + record.income_others

    total_expenses = fields.Float(compute='_total_expenses')
    @api.depends('expenses_rent','expenses_allowances','expenses_services','expenses_others')
    def _total_expenses(self):
        for record in self:
            record.total_expenses = record.expenses_rent + record.expenses_allowances + record.expenses_services + record.expenses_others

    expenses_rent = fields.Float(string='Expenses Rent', required=True, default=0);
    expenses_allowances = fields.Float(string='Expenses Allowances', required=True, default=0);
    expenses_services = fields.Float(string='Expenses Services', required=True,default=0);
    expenses_others = fields.Float(string='Expenses Others', required=True,default=0);

    tag_ids = fields.Many2many('loanapp_tag', string='Tags')
    guarantor_ids = fields.One2many('loanapp_guarantor','loanapp_application_id', string='Guarantors')
    loanapp_repay_plan_ids= fields.One2many('loanapp_repayplan','loanapp_application_id',string='Loanapp Repay')
    def action_accept(self):
        for record in self:
            record.status = 'b'
        return True
    def action_approve(self):
        for record in self:
            record.status = 'c'
        return True
    def action_disburse(self):
        for record in self:
            record.status = 'd'

        return True
    def action_cancel(self):
        for record in self:
            record.status = "x"
            return True
    def action_loanapp_application_stat_button(self):
         for record in self:
             return True

# TAREA: Ver como se genera el Boton Stat

    # need to recalculate loan schedule plan
    # 0. Agregar Downpayment en el producto

    # 1. Calcular las fechas de inicio plan pagos con base en desembolso, y
    # frecuencia de pago


    def action_calc_loan_scheld(self):

        for record in self:
            # cleans the current loan application plan
            self.env.cr.execute(f"DELETE FROM loanapp_repayplan WHERE loanapp_application_id={record.id}" )

            # here only when term is given
            if record.term > 0:
                plan = calc_installment_plan(record.apply_amount,record.interest_rate,record.term, record.term_type)
                for x in plan:
                    self.env['loanapp_repayplan'].create({
                            'loanapp_application_id': record.id,
                            'payment_number': x["payment_number"],
                            'date_start': fields.Date.today(),
                            'date_end': fields.Date.today(),
                            'repay_amount': x["repay_amount"],
                            'principal_amount': x["principal_amount"],
                            'interest_amount': x["interest_amount"],
                            'tax_amount': 0,
                            'loan_balance': x["loan_balance"],
                    })

            # if term is not given, need to have proposed repay amount
            if record.term == 0:
                self.env['loanapp_repayplan'].create({
                    'loanapp_application_id': record.id,
                    'payment_number': 1,
                    'date_start': fields.Date.today(),
                    'date_end': fields.Date.today(),
                    'repay_amount': x.repay_amount,
                    'principal_amount': x.principal_amount,
                    'interest_amount': x.interest_amount,
                    'tax_amount': 0,
                    'loan_balance': x.loan_balance
                })

            return True

def calc_installment(principal, interest_rate, term, term_type="m"):
    # Convertir la tasa anual según el tipo de periodo
    if term_type == "m":
        rate_per_periodo = interest_rate / 12 / 100
    elif term_type == "w":
        rate_per_periodo = interest_rate / 52 / 100
    elif term_type == "q":
        rate_per_periodo = interest_rate / 26 / 100
    else:
        raise ValidationError("Term type not supported, please use 'Monthly', 'Weekly' o 'Bimonthly'.")

    # Calcular el pago del periodo usando la fórmula de amortización francesa
    installment = (principal * rate_per_periodo) / (1 - (1 + rate_per_periodo) ** -term)
    return installment


def calc_installment_plan(principal, interest_rate, term, term_type="m"):
    # Convertir la tasa anual según el tipo de periodo
    if term_type == "m":
        rate_per_periodo = interest_rate / 12 / 100
    elif term_type == "w":
        rate_per_periodo = interest_rate / 52 / 100
    elif term_type == "q":
        rate_per_periodo = interest_rate / 26 / 100
    else:
        raise ValidationError("Term type not supported, please use 'Monthly', 'Weekly' o 'Bimonthly'.")

    # Calcular el pago del periodo usando la fórmula de amortización francesa
    installment = (principal * rate_per_periodo) / (1 - (1 + rate_per_periodo) ** -term)

    # Inicializar lista para almacenar los datos de cada periodo
    installment_plan = []

    balance = principal
    for periodo in range(1, term + 1):
        # Calcular interés del periodo
        interes_periodo = balance * rate_per_periodo
        # Calcular la parte de la cuota que amortiza el capital
        amortizacion_periodo = installment - interes_periodo
        # Calcular el saldo restante
        balance -= amortizacion_periodo

        # Guardar el resultado en el plan de amortización
        installment_plan.append({
            "payment_number": periodo,
            "repay_amount": round(installment, 2),
            "interest_amount": round(interes_periodo, 2),
            "principal_amount": round(amortizacion_periodo, 2),
            "loan_balance": round(balance, 2)
        })

    return installment_plan


def calc_term(principal, interest_rate, repay_amount, term_type="m"):
    # Convertir la tasa anual según el tipo de periodo
    if term_type == "m":
        rate_per_period = interest_rate / 12 / 100
    elif term_type == "w":
        rate_per_period = interest_rate / 52 / 100
    elif term_type == "q":
        rate_per_period = interest_rate / 26 / 100
    else:
        raise ValidationError("Term type not supported, please use 'Monthly', 'Weekly' o 'Bimonthly'.")

    # Verificar que la cuota sea suficiente para cubrir los intereses
    if repay_amount <= principal * rate_per_period:
        raise ValidationError("Installment amount is too low to cover interest. Please provide a higher amount.")

    # Calcular el número de periodos
    terms = math.log(repay_amount / (repay_amount - principal * rate_per_period)) / math.log(1 + rate_per_period)

    return math.ceil(terms)  # Redondear hacia arriba para obtener el número de periodos completo


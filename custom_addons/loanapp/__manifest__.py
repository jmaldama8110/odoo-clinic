{
    'name': "Loan Application Manager",
    'summary': 'Track loans and credit accounts',
    'description': "Loan Application Manager is designed for financial services companies",
    'website': 'https://www.orion10x.net/odoo_loan_app_manager',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/loanapp_application_views.xml',
        'views/loanapp_application_menu.xml',
        'views/loanapp_product_views.xml',
        'views/loanapp_product_menu.xml',
        'views/loanapp_tag_views.xml',
        'views/loanapp_tag_menu.xml',
        'views/loanapp_guarantor_views.xml',
        'views/loanapp_repay_plan_views.xml',
        'views/loanapp_balance_views.xml',
        'views/loanapp_balance_menu.xml'
    ]
}
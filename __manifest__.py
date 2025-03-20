{
    'name': 'Custom Invoice Sales Relationship',
    'version': '17.0.1.0.0',
    'category': 'Sales/Accounting',
    'summary': 'Permite que una factura agrupe múltiples órdenes de venta.',
    'description': '''
        Este módulo personaliza la facturación permitiendo que una factura
        agrupe múltiples órdenes de venta relacionadas a un mismo cliente,
        sin alterar la lógica original de Odoo.
    ''',
    'author': 'Alphaqueb Consulting',
    'depends': ['sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

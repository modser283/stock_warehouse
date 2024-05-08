{
    'name': "stock_warehouse_transfer",
    'author': "",
    'category': '',
    'version': '15.0',
    'depends': ['base', 'sale_management', 'account', 'mail','contacts','stock'
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/res_config_settings_views.xml',
        'views/stock_warehouse_transfer_view.xml',
        'views/stock_location_view.xml',
    ],
    'application': False,
}
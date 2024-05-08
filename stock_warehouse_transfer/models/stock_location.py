from odoo import api, fields, models, _, exceptions


class StockLocation(models.Model):
    _inherit = 'stock.location'

    authorized_users = fields.Many2many('res.users', string='Authorized Users')

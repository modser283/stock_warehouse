from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    stock_location_id = fields.Many2one('stock.location')


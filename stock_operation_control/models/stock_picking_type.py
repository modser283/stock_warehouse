from odoo import api, fields, models, _



class StockPickingType(models.Model):
    _inherit = ['stock.picking.type']

    not_allowed_more_demand = fields.Boolean(string='Not Allowed More Than Demand')
    not_allowed_less_demand = fields.Boolean(string='Not Allowed Less Than Demand')







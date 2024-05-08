# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    transient_location = fields.Many2one('stock.location', string='Transient Location',
                                         config_parameter='stock_warehouse_transfer.transient_location',
                                         related='company_id.stock_location_id', readonly=False)


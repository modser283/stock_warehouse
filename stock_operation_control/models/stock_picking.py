from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #check if quantity more than demand if configure could not allowed that
    def check_quantity_more(self):
        for rec in self:
            if rec.picking_type_id.not_allowed_more_demand:
                    for move in rec.move_ids_without_package:
                         if move.quantity_done > move.product_uom_qty:
                             raise ValidationError(_('Quantity done cannot be more than demand quantity.'))



    # check if quantity less than demand if configure could not allowed that
    def check_quantity_less(self):
        for rec in self:
            if rec.picking_type_id.not_allowed_less_demand:
                    for move in rec.move_ids_without_package:
                         if move.quantity_done < move.product_uom_qty:
                             raise ValidationError(_('Quantity done cannot be less than demand quantity.'))


    #if you dont understand this block, dont ask me ask china
    def button_validate(self):
        self.check_quantity_less()
        self.check_quantity_more()
        return super().button_validate()
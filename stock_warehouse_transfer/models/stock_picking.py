from odoo import models, api, exceptions, fields
from odoo.exceptions import UserError
class StockPicking(models.Model):
    _inherit = 'stock.picking'


    stock_transfer_id = fields.Many2one('stock.warehouse.transfer', string='Stock Transfer Id')


    def button_validate(self):
        for picking in self:
            authorized_users = picking.location_id.authorized_users.ids
            current_user = self.env.user.id
            if current_user not in authorized_users:
                raise exceptions.UserError(_("You are not authorized to validate transfers for this location."))
        return super(StockPicking, self).button_validate()


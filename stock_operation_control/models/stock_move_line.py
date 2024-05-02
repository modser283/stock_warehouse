from odoo import api, fields, models, _, exceptions


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, values):
        if 'picking_id' in values:
            picking_type_code = self.env['stock.picking'].browse(values.get('picking_id')).picking_type_id.code
            if picking_type_code in ['incoming', 'outgoing']:
                has_qroup = self.env.user.has_group('stock_operation_control.stock_move_line_manager_group')
                if not has_qroup and not values.get('sale_line_id', False) and not values.get('purchase_line_id', False):
                    raise exceptions.AccessError(_("You are not allowed to add new lines to this type of operation."))
        return super(StockMove, self).create(values)

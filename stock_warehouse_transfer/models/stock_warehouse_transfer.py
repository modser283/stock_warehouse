from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StockWarehouseTransfer(models.Model):
    _name = 'stock.warehouse.transfer'
    _description = 'Transfer Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    ref = fields.Char(readonly=1, string="Reference", default='New',)

    @api.model
    def _get_default_created_by(self):
        return self.env["res.users"].browse(self.env.uid)

    created_by = fields.Many2one(comodel_name="res.users", required=True, copy=False, tracking=True, default=_get_default_created_by, string='Responsible')
    source_location_id= fields.Many2one('stock.location', string='Source Location', domain="[('location_id.usage', '=', 'internal')]")
    def _default_transient_stock(self):
        stock_location_id = self.env.company.stock_location_id
        return stock_location_id

    destination_location_id = fields.Many2one('stock.location', string='Destination Location',
                                              domain="[('location_id.usage', '=', 'internal')]")
    transient_location = fields.Many2one('stock.location', string='Transient Location', default = _default_transient_stock)
    transfer_date = fields.Datetime(string='Schedule Date')
    picking_type = fields.Many2one('stock.picking.type', string='Operation Type')
    # , domain = "[('picking_type_id.code', '=', 'internal')]"
    product_line = fields.One2many('product.line', 'product_warehouse_id', string="Product Line", required=1)
    stock_picking_ids = fields.One2many('stock.picking', 'internal_transfer_order_id', string='Stock Pickings')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transport', 'In Transport'),
        ('done', 'Done'),
    ], default='draft', tracking=1, string="Status")

    def action_draft(self):
        pass

    # when i wrote this code, only God & I understood what it did..
    # Now.. only God knows.

    def action_confirmed(self):

        mylist = []
        for stock_line in self.product_line:

            mylist.append(
                (0, 0, {'product_id': stock_line.stock_product_id.id, 'name': stock_line.stock_product_id.name,
                        'product_uom_qty': stock_line.demand, 'location_id': self.source_location_id.id,
                        'product_uom': stock_line.product_uom.id,
                        'location_dest_id': self.transient_location.id, }))
        rec = self.env['stock.picking'].create(
            {'picking_type_id': self.picking_type.id, 'location_id': self.source_location_id.id,
             'location_dest_id': self.transient_location.id, 'scheduled_date': self.transfer_date,'stock_transfer_id' : self.id,
             'move_ids_without_package': mylist})
        return rec

        # Set the state of the created picking to 'Ready'
        if len(move_ids_without_package) == 0:
            raise ValidationError(_("Enter vaild number of product "))
        else:
            rec.action_assign()
            rec.action_confirm()

        self.write({'state': 'confirmed'})

    def action_in_transport(self):
        pass


    def show_stock_pickings(self):
        """
        Method to open stock pickings related to this internal transfer order.
        """
        pickings = self.stock_picking_ids
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('id', 'in', pickings.ids)]
        return action

    @api.model
    def create(self, vals):
        res = super(StockWarehouseTransfer, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('stock.transfer.seq')
        return res


class StockPicking(models.Model):
    _inherit = "stock.picking"


    internal_transfer_order_id = fields.Many2one('stock.warehouse.transfer', string='Internal Transfer Order')


    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            rec.picking_id.stock_transfer_id.state = 'in_transport'
        return res

class ProductLine(models.Model):
    _name = 'product.line'

    product_warehouse_id = fields.Many2one('stock.warehouse.transfer', tracking=1)
    stock_product_id = fields.Many2one('product.product', required=1)
    product_uom = fields.Many2one('uom.uom', strong='UOM', related='stock_product_id.uom_id', readonly=True)
    demand = fields.Integer(tracking=1, default=1, string="Demand")
    done = fields.Integer(tracking=1, default=1, string="Done")

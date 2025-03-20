from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_ids = fields.Many2many('sale.order', string="Órdenes de Venta Relacionadas")

    @api.model
    def create(self, vals):
        """Al crear una factura, asignar las órdenes de venta asociadas."""
        move = super().create(vals)
        if 'invoice_line_ids' in vals:
            sale_order_ids = []
            for line in move.invoice_line_ids:
                sale_order_ids.extend(line.sale_line_ids.mapped('order_id').ids)
            move.sale_order_ids = [(6, 0, list(set(sale_order_ids)))]
        return move

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_ids = fields.Many2many('sale.order', string="Órdenes de Venta Relacionadas")

    @api.model
    def create(self, vals):
        move = super().create(vals)
        if 'invoice_line_ids' in vals:
            sale_order_ids = []
            for line in move.invoice_line_ids:
                sale_order_ids.extend(line.sale_line_ids.mapped('order_id').ids)
            if sale_order_ids:
                move.sale_order_ids = [(6, 0, list(set(sale_order_ids)))]
                self.env['sale.order'].browse(sale_order_ids).write({
                    'invoice_ids': [(4, move.id)],
                    'invoice_status': 'invoiced'
                })
        return move

    def write(self, vals):
        res = super().write(vals)
        if 'sale_order_ids' in vals:
            for move in self:
                # Aquí la corrección clave: [move.id] en lugar de move.id
                old_orders = self.env['sale.order'].search([('invoice_ids', 'in', [move.id])])

                # Desvincular las órdenes que ya no están relacionadas
                old_orders.filtered(lambda o: o.id not in move.sale_order_ids.ids).write({
                    'invoice_ids': [(3, move.id)],
                    'invoice_status': 'to invoice'
                })

                # Vincular nuevas órdenes relacionadas
                new_orders = move.sale_order_ids
                new_orders.write({
                    'invoice_ids': [(4, move.id)],
                    'invoice_status': 'invoiced'
                })
        return res

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many('account.move', string="Facturas Relacionadas")

    def action_create_invoice(self):
        """Generar factura agrupada desde las órdenes seleccionadas."""
        orders = self.filtered(lambda o: o.invoice_status != 'invoiced')

        if not orders:
            raise UserError("Todas las órdenes seleccionadas ya están facturadas.")

        partners = orders.mapped('partner_id')
        if len(partners) > 1:
            raise UserError("Selecciona solo órdenes del mismo cliente para facturar juntas.")

        invoice_vals = {
            'partner_id': partners.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [],
        }

        for order in orders:
            for line in order.order_line:
                invoice_vals['invoice_line_ids'].append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'tax_ids': [(6, 0, line.tax_id.ids)],
                    'sale_line_ids': [(6, 0, [line.id])]
                }))

        invoice = self.env['account.move'].create(invoice_vals)

        orders.write({
            'invoice_ids': [(4, invoice.id)],
            'invoice_status': 'invoiced'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura Creada',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current'
        }

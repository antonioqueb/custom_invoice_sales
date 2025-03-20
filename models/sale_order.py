from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many('account.move', string="Facturas Relacionadas", readonly=True)

    def action_create_invoice(self):
        """Generar factura agrupada para múltiples órdenes del mismo cliente."""
        orders = self.search([
            ('partner_id', '=', self.partner_id.id), 
            ('invoice_status', '!=', 'invoiced')
        ])

        if not orders:
            return

        invoice_vals = {
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [],
        }

        for order in orders:
            for line in order.order_line:
                invoice_vals['invoice_line_ids'].append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'sale_line_ids': [(6, 0, [line.id])]
                }))

        invoice = self.env['account.move'].create(invoice_vals)

        orders.write({
            'invoice_ids': [(4, invoice.id)],
            'invoice_status': 'invoiced'
        })

        return invoice

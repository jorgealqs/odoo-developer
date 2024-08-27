import logging
from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        for record in self:
            # Llamar al método original para cambiar el estado
            super(InheritedEstateProperty, record).action_sold_property()

            # Verificar que la propiedad tiene un precio de venta y
            # un comprador
            if not record.selling_price or not record.buyer:
                raise UserError(
                    "The property must have a selling price and a buyer to"
                    " create an invoice."
                )

            # Crear las líneas de factura
            invoice_line_values = [
                {
                    'name': 'Property Sale (6% of Selling Price)',
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06,
                },
                {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }
            ]

            # Crear la factura (account.move) con las líneas de factura
            move_values = {
                'partner_id': record.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, line) for line in invoice_line_values
                ],
            }
            self.env['account.move'].create(move_values)
            _logger.info(f"Invoice created for property: {record.name}")

        return True

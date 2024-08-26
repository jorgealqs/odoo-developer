from odoo import models, fields, api  # noqa: F401
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_deadline',
        inverse='_inverse_deadline',
        store=True
    )

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date + timedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Date.today() + timedelta(days=record.validity)
                )

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    # Convert create_date to date for comparison
                    create_date = record.create_date.date()
                    delta = record.date_deadline - create_date
                    record.validity = delta.days
                else:
                    # Si no hay create_date, calculamos la
                    # validez basada en hoy
                    delta = record.date_deadline - fields.Date.today()
                    record.validity = delta.days

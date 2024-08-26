from odoo import models, fields, api  # noqa: F401
from datetime import timedelta
from odoo.exceptions import UserError


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

    def action_confirm_offer(self):
        for record in self:
            # Verificar si la oferta ya está aceptada
            if record.property_id.offer_ids.filtered(
                lambda o: (
                    o.status == 'accepted' and o.id != record.id
                    )
            ):
                raise UserError("This property already has an accepted offer.")
            # Si la oferta no está aceptada, procede a aceptarla
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

    def action_refused_offer(self):
        for record in self:
            record.status = 'refused'

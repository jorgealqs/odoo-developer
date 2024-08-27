from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many(
        'estate.property',
        inverse_name='property_type_id',
        string='Properties'
    )
    sequence = fields.Integer(
        default=1,
        help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        inverse_name='property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string='Offers'
    )

    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name is unique!!!'
        )
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

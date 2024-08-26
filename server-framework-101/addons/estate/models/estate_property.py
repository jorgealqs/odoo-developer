from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Date of Availability',
        copy=False,
        default=lambda self: datetime.today() + timedelta(days=90)
        # Default to 3 months from today
    )  # copy=False, Prevent copying
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        string='Selling Price',
        readonly=True,
        copy=False,
    )  # Read-only and prevent copying
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2
    )
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(string='Active', default=True)
    # Active field with a default of True
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
    )
    buyer = fields.Many2one(
        'res.partner',
        string="Buyer"
    )
    salesperson = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags',
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Property Offers',
    )
    total_area = fields.Integer(
        string="Total Area",
        compute='_compute_total_area',
        store=True,
    )
    best_price = fields.Float(
        string="Best Price",
        compute='_compute_best_price',
        store=True,
        readonly=True,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            living_area = record.living_area or 0
            garden_area = record.garden_area or 0
            record.total_area = living_area + garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                prices = record.offer_ids.mapped('price')
                if prices:
                    record.best_price = max(prices)
                else:
                    record.best_price = 0.0  # O cualquier valor
                    # predeterminado que desees
            else:
                record.best_price = 0.0  # O cualquier valor predeterminado
                # que desees si no hay ofertas

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled.")
            record.state = "canceled"

    def action_sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be set as sold.")
            record.state = "sold"

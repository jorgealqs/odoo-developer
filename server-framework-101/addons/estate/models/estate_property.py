from odoo import models, fields
from datetime import datetime, timedelta


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

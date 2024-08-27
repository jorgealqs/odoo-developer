from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The name is unique!!!',
        )
    ]

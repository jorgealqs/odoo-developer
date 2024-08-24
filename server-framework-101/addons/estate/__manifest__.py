{
    "name": "Real Estate",
    "version": "1.0",
    "author": "Jorge Alberto Quiroz Sierra",
    "sequence": -10,
    'category': 'Odoo/Tutorials',
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        # "views/estate_property_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "description": """
        Estate Management System is an
        application that allows users to manage properties,
        property types, property tags, property offers,
        and inherit data from the base module.
    """
}

{
    "name": "Owl Components",
    "version": "1.0",
    "author": "Jorge Alberto Quiroz Sierra",
    "sequence": -12,
    'category': 'Odoo/Tutorials',
    "depends": ["base", "web"],
    "installable": True,
    "auto_install": False,
    "application": True,
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'awesome_owl.assets_playground': [
            # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap_backend'),

            # required for fa icons
            'web/static/src/libs/fontawesome/css/font-awesome.css',

            # include base files from framework
            ('include', 'web._assets_core'),

            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',
            'awesome_owl/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}

# This is the manifest file, it's a key component of a module in Odoo.

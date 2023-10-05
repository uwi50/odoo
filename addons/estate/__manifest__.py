{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "U Elvis",
    'category': 'Real Estate/Brokerage',
    'description': """
    the form view summarizes important information for the property, such as the name, the property type, 
    the postcode and so on. The first tab contains information describing the property: bedrooms, living area, 
    garage, garden.
    The second tab lists the offers for the property. We can see here that potential buyers can make offers above or 
    below the expected selling price. It is up to the seller to accept an offer.
    """,
    # data files always loaded at installation
    'data': [
        #'views/mymodule_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/inherited_res_users_views.xml',
        'report/estate_report_templates.xml',
        'report/estate_reports_actions.xml',
        'views/estate_menus.xml',
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        #'demo/demo_data.xml' ,
        'data/estate_demo.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

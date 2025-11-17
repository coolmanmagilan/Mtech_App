{
    "name": "Mtech Setup",
    "description": """Setup Sheet for Mtech""",
    "version": "1.0",
    "author": "Magilan Vasanthakumar",
    "website": "www.mtech_setup.com",
    "category": "Inventory",
    "depends": [],
    "data": [
        'security/ir.model.access.csv',
        'data/ToolType.xml',
        'views/ToolList_view.xml',
        'views/SetupSheet_view.xml',
        'report/SetupSheetReport.xml',
        'views/menu_items.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'Mtech_Setup/static/ToolPart_Image.css',
            ],
        },

    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
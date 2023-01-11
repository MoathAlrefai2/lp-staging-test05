{
    'name':"lp_helpdesk",
    "description":'(lp_helpdesk) inherit from (helpdesk.ticket)',
    'summary': """
      Modifications for helpdesk module, https://leading-point.com/""",

    'description': """
      Modifications  for helpdesk
  """,
'version':'14.0.1.1',

    'author': "Leading Point",
    'website': "https://leading-point.com",
     'version': '14.0.3',
 'data': [
'security/ir.model.access.csv',
'views/lp_helpdesk.xml'
    ],
    'qweb': [
        "static/src/xml/helpdesk_team_templates.xml",
    ],
     'category': 'Leading Point',
    'depends':[
         'base_setup',
        'mail',
        'utm',
        'rating',
        'web_tour',
        'resource',
        'portal',
        'digest',
        'helpdesk',
        'helpdesk_timesheet',
        'sale_timesheet_enterprise'
    ]
}

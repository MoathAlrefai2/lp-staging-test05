{
    'name':"lp_contact",
    "description":'(lp_contact) inherit from (res.partner)',
    'summary': """
      Modifications for contact module , https://leading-point.com/""",

    'description': """
      Modifications for contact
  """,

    'author': "Leading Point",
    'website': "https://leading-point.com",
 'data': ['views/lp_contact.xml',
'views/lp_attribute.xml',
'data/positions.xml',
'security/ir.model.access.csv' ],
 'version': '14.0.4',
     'category': 'Leading Point',
    'depends':['base','contacts','hr']
}

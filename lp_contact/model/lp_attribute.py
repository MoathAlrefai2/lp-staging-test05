from datetime import datetime, timedelta
from odoo import models, fields



class Attribute(models.Model):
    _name = "lp.attribute"

    name = fields.Char(string='Name')

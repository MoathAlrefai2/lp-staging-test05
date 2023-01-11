from datetime import datetime, timedelta
from odoo import models, fields


class ExcludedModels(models.Model):
    _name = "excluded.models"

    models = fields.Many2one('ir.model', string="Models")
    model_name = fields.Char(string='Model Name', related='models.model', store=True)

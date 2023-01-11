# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields


class DeletedRecords(models.Model):
    _name = "deleted.records"
    _description = "Stores deleted records."

    name = fields.Char(string="Name")
    model_id = fields.Many2one('ir.model', string="Model")
    user_id = fields.Many2one('res.users', string="Deleted By")
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, index=True,
                                 default=lambda self: self.env.user.company_id,
                                 help="Company related to this journal")


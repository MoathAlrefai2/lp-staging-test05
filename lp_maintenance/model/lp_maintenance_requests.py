from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class LP_MaintenanceRequests(models.Model):
    _inherit = 'maintenance.request'
    lp_assets = fields.Many2one('asset.management')


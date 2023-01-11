from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class LP_Contact(models.Model):
    _inherit = 'res.partner'
    lp_label_name = fields.Char('label for name.', default='ind_', readonly=True)
    lp_name = fields.Char('name label', compute='onchange_name')

    lp_attributes = fields.Many2many('lp.attribute')
    referred = fields.Char('Referred By')
    lp_domain = fields.Char("Domain")
    lp_ranking = fields.Selection([('a', 'A'),
                                   ('b', 'B'),
                                   ('c', 'C'),
                                   ('d', 'D')],
                                  string='Ranking', required=True, default='a')

    @api.depends('lp_name')
    def onchange_name(self):
        prefix = "ind_"
        if self.company_type == 'person':
            self.lp_name = prefix + self.name
        else:
            self.lp_name = self.name

    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            vals.update({"user_id": self._uid})
        return super(LP_Contact, self).create(vals)
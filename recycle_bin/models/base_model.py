# -*- coding: utf-8 -*-
import os
from odoo import api, models



class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'

    def unlink(self):
        # common unlink method override.
        deleted_recs = self.sudo().env['deleted.records']

        ''' If user will delete records from below list than history record will
            created '''
        excluded_models = self.sudo().env['excluded.models'].search([]).mapped('model_name')

        if self and not self._transient and self._name not in excluded_models:

            model_name = self._name
            # Fetch models id of deleted record.
            model_rec = self.env['ir.model'].sudo().search(
                [('model', '=', model_name)])
            '''Get display name of deleted records to write in
                deleted_records models.'''
            for rec in self:
                name = False
                if rec._fields.get('name'):
                    if rec.name:
                        name = rec.name + ', ' + str(rec.id)
                if not name and self._fields.get('display_name'):
                    if rec.display_name:
                        name = rec.display_name + ', ' + str(rec.id)
                if not name and self._rec_name:
                    sql_query = '''SELECT %s from %s where id = %s'''
                    params = (self._rec_name, self._table, rec.id)
                    self.env.cr.execute(sql_query, params)
                    results = self.env.cr.dictfetchall()
                    name = results[0].get(self._rec_name)
                    name += ', ' + str(rec.id)

                # Created deleted history record.
                deleted_rec = deleted_recs.sudo().create(
                    {'name': name,
                     'model_id': model_rec.id,
                     'user_id': self.env.user.id})

        return super(BaseModelExtend, self).unlink()

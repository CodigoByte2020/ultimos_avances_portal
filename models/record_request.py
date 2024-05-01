from odoo import fields, models


class RecordRequest(models.Model):
    _name = 'record.request'
    _rec_name = 'op_admission_id'

    op_admission_id = fields.Many2one(comodel_name='op.admission', string='Admisión', required=True)
    partner_id = fields.Many2one(related='op_admission_id.partner_id', store=True)
    batch_id = fields.Many2one(related='op_admission_id.batch_id')
    course_id = fields.Many2one(related='op_admission_id.course_id')
    application_number = fields.Char(related='op_admission_id.application_number')
    description = fields.Html(string='Descripción')

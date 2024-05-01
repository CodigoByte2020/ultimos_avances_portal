from odoo import api, fields, models

STATE_SELECTION = [
    ('on_hold', 'En espera'),
    ('accepted', 'Aceptado'),
    ('observed', 'Observado'),
]

REASON_FOR_OBSERVATION_SELECTION = [
    ('incorrect_format', 'No está cargado en un formato correcto'),
    ('poor_readability', 'Legibilidad deficiente'),
    ('incorrect_document', 'Documento incorrecto')
]


class ResPartnerDocument(models.Model):
    _name = 'res.partner.document'

    partner_id = fields.Many2one(comodel_name='res.partner')
    document = fields.Char(string='Documento', readonly=True)
    filename = fields.Char(string='Nombre de archivo')
    file = fields.Binary(attachment=True, string='Archivo')
    state = fields.Selection(selection=STATE_SELECTION, default='on_hold', string='Estado')  # TODO: FALTA MANEJAR LA VISIBIVILIDAD DE LOS BOTONES
    reason_for_observation = fields.Selection(selection=REASON_FOR_OBSERVATION_SELECTION,
                                              string='Motivos de obervación')
    attachment_id = fields.Many2one(comodel_name='ir.attachment')

    @api.model
    def create(self, values):
        rec = super(ResPartnerDocument, self).create(values)
        attachment = self.env['ir.attachment'].sudo().search([('res_id', '=', self.id)])
        return rec

    def write(self, values):
        # values.update({'res_partner_document': self.id})
        rec = super(ResPartnerDocument, self).write(values)
        attachment = self.env['ir.attachment'].sudo().search([('res_id', '=', self.id)])
        return rec

    # @api.depends('file')
    # def _compute_attachment_id(self):
    #     for rec in self:
    #         attachment_id = self.env['ir.attachment'].sudo().search([
    #             ('res_model', '=', self._name),
    #             ('res_id', '=', rec.id)
    #         ])
    #         rec.update({'attachment_id': attachment_id})

    def action_observe(self):
        attachment_id = self.env['ir.attachment'].sudo().search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id)
        ])
        view_id = self.env.ref('isep_record_request.observe_partner_document_wizard_view_form').id
        return {
            'name': 'Observar documento',
            'type': 'ir.actions.act_window',
            'res_model': 'observe.partner.document.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {'default_res_partner_document_id': self.id}
        }

    def action_accept(self):
        self.write({'state': 'accepted'})

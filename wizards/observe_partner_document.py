from odoo import fields, models

REASON_FOR_OBSERVATION_SELECTION = [
    ('incorrect_format', 'No está cargado en un formato correcto'),
    ('poor_readability', 'Legibilidad deficiente'),
    ('incorrect_document', 'Documento incorrecto')
]


class ObservePartnerDocumentWizard(models.TransientModel):
    _name = 'observe.partner.document.wizard'

    res_partner_document_id = fields.Many2one(comodel_name='res.partner.document')
    reason_for_observation = fields.Selection(selection=REASON_FOR_OBSERVATION_SELECTION, string='Motivo de obervación',
                                              required=True)

    def add_comment(self):
        '''
            Creates a record in mail.message with the comment added in the wizard.
            Modify the state of res_partner_document to observed.
            :return: None
        '''
        partner_id = self.res_partner_document_id.partner_id
        reason_for_observation = dict(self._fields['reason_for_observation'].selection)\
            .get(self.reason_for_observation, '')
        body = '''
            <p>Observación en adjunto: <strong>{}</strong></p>
            <p>Detalle:</p>
            <p class="text-danger"><strong>{}</strong></p>
        '''.format(self.res_partner_document_id.document, reason_for_observation)
        self.env['mail.message'].create({
            'message_type': 'comment',
            'model': 'res.partner',
            'res_id': partner_id.id,
            'subject': partner_id.name,
            'subtype_id': self.env.ref('mail.mt_comment').id,
            'author_id': partner_id.id,
            'body': body
        })
        self.res_partner_document_id.write({
            'state': 'observed',
            'reason_for_observation': self.reason_for_observation
        })

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birth_date = fields.Date('Fecha de nacimiento', required=True)
    res_partner_document_ids = fields.One2many(comodel_name='res.partner.document', inverse_name='partner_id')

    @api.model
    def create(self, values):
        self.create_res_partner_document(values)
        rec = super(ResPartner, self).create(values)
        return rec

    def write(self, values):
        self.create_res_partner_document(values)
        rec = super(ResPartner, self).write(values)
        return rec

    def create_res_partner_document(self, values):
        country_id = values.get('country_id', False)
        if country_id:
            res_partner_document_ids = []
            country = self.env['res.country'].browse(country_id)
            record_request_list_model = self.env['record.request.list']
            list_of_mexican_documents = record_request_list_model.search([('is_list_of_mexican_documents', '=', True)],
                                                                         limit=1)
            list_of_foreign_documents = record_request_list_model.search([('is_list_of_mexican_documents', '=', False)],
                                                                         limit=1)

            if not list_of_mexican_documents:
                raise ValidationError('¡Debes crear una Lista de solicitudes de registro para documentos mexicanos!')
            if not list_of_foreign_documents:
                raise ValidationError('¡Debes crear una Lista de solicitudes de registro para documentos extranjeros!')

            if country.code == 'MX':
                record_request_list_id = list_of_mexican_documents
            else:
                record_request_list_id = list_of_foreign_documents

            self.res_partner_document_ids.unlink()
            for line in record_request_list_id.record_request_list_line_ids:
                res_partner_document_ids.append((0, 0, {'document': line.document}))

            values.update({'res_partner_document_ids': res_partner_document_ids})

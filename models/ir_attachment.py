from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    res_partner_document_id = fields.Many2one(comodel_name='res.partner.document')

    # @api.model
    # def create(self, values):
    #     attachments = self.env['ir.attachment'].sudo().search([('res_model', '=', 'res.partner.document')])
    #     if attachments:
    #         pass
    #     # res_partner_document_id = self._context.get('res_partner_document_id', False)
    #     # values.update({'res_partner_document_id': res_partner_document_id})
    #     res_partner_document = values.get('res_partner_document', False)
    #     rec = super(IrAttachment, self).create(values)
    #     return rec
    #
    # def write(self, values):
    #     rec = super(IrAttachment, self).write(values)
    #     return rec

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        ret = super(IrAttachment, self).search(args, offset=offset, limit=limit, order=order, count=count)
        # if self.env.context.get('from_mass_mailing_cron'):
        #     ret = ret.filtered(lambda m: m.mailing_type != 'whatsapp' or m.state not in ['in_queue', 'sending'])
        print()
        return ret


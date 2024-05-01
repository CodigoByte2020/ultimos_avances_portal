/** @odoo-module **/

import { BinaryField } from "@web/views/fields/binary/binary_field";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import rpc from 'web.rpc';

patch(BinaryField.prototype, 'attachment_preview2', {
    setup() {
        this._super(...arguments);
        this.messaging = useService("messaging");
    },
    async _onFilePreview(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var self = this;
        var match = false;
//        if (self.props.record.data.mimetype && self.props.record.data.mimetype != undefined){
//            match = self.props.record.data.mimetype.match("(image|video|application/pdf|text)");
//        }
        //TODO: VERIFICAR LOS MIMETYPES
        let data = self.props.record.data;
        let result = await self.rpc({
            model: 'ir.attachment',
            method: 'search_read',
            domain: [[self.props.record.resModel, '=', 'res.partner.document'], ['res_id', '=', data.id]]
        })

        if (self.props.record.data.filename && self.props.record.data.filename != undefined) {
            const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt'];
            if (allowedExtensions.some(ext => self.props.record.data.filename.toLowerCase().endsWith(ext))) {
                alert('Este tipo de archivo está soportado')
                match = true
            }
        }

        if (match) {
            this.messaging.get().then((messaging) => {
                const attachmentList = messaging.models["AttachmentList"].insert({
                    selectedAttachment: messaging.models["Attachment"].insert({
                        id: this.props.record.data.id,
                        filename: this.props.record.data.name,
                        name: this.props.record.data.name,
                        mimetype: this.props.record.data.mimetype,
                    }),
                });
                this.dialog = messaging.models["Dialog"].insert({
                    attachmentListOwnerAsAttachmentView: attachmentList,
                });
            });
        } else {
            alert('This file type is not supported.')
        }
    },
    getMessaging() {
        return this.env.services.messaging && this.env.services.messaging.modelManager.messaging;
    },
})

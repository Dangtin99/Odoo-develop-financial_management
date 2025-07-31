from odoo import models, fields

class TuniOrderWizard(models.TransientModel):
    _name = 'tuni.order.wizard'
    _description = 'Chọn Ngày Order'
    ngay_chon = fields.Date(string='Chọn ngày', required=True)

    def action_xem_ngay_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ngày Order',
            'res_model': 'tuni.order',
            'view_mode': 'kanban,form',
            'domain': [('ngay_order', '=', self.ngay_chon)],
            'context': {'default_ngay_order': self.ngay_chon},
           
        }

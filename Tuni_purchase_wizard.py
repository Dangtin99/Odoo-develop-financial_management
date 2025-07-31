from odoo import models, fields

class TuniPurchaseWizard(models.TransientModel):
    _name = 'tuni.purchase.wizard'
    _description = 'Chọn Ngày Mua Hàng'
    ngay_chon = fields.Date(string='Chọn ngày', required=True)

    def action_xem_mua_hang(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ngày Mua Hàng',
            'res_model': 'tuni.purchase',
            'view_mode': 'list,form',
            'domain': [('ngay_mua', '=', self.ngay_chon)],
             'context': {
                'default_ngay_mua': self.ngay_chon
            }
        }

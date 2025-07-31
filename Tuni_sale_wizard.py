from odoo import models, fields

class TuniSaleWizard(models.TransientModel):
    _name = 'tuni.sale.wizard'
    _description = 'Chọn ngày giao dịch bán hàng'

    ngay_chon = fields.Date(string='Chọn ngày', required=True)

    def action_xem_ban_hang(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Giao dịch bán hàng',
            'res_model': 'tuni.sale',
            'view_mode': 'list,form',
            'domain': [('ngay_ban', '=', self.ngay_chon)],
            'target': 'current',
            'context': {
                'default_ngay_ban': self.ngay_chon
            }
        }

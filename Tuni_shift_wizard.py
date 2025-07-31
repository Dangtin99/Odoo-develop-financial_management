from odoo import models, fields

class TuniShiftWizard(models.TransientModel):
    _name = 'tuni.shift.wizard'
    _description = 'Chọn Ngày Phân Ca'

    ngay_chon = fields.Date(string='Chọn ngày', required=True)

    def action_xem_phan_ca(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ngày Phân Ca',
            'res_model': 'tuni.shift',
            'view_mode': 'list,form',
            'domain': [('ngay_lam', '=', self.ngay_chon)],
            'context': {
                'default_ngay_lam': self.ngay_chon
            }
        }

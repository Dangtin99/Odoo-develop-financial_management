from odoo import models, fields

class TuniAttendanceWizard(models.TransientModel):
    _name = 'tuni.attendance.wizard'
    _description = 'Chọn Ngày Chấm Công'

    ngay_chon = fields.Date(string='Chọn ngày', required=True)

    def action_xem_cham_cong(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ngày Chấm Công',
            'res_model': 'tuni.attendance',
            'view_mode': 'list,form',
            'domain': [('ngay_cham_cong', '=', self.ngay_chon)],
            'context': {
                'default_ngay_cham_cong': self.ngay_chon
            }
        }
            

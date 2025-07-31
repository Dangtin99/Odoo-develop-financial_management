from odoo import models, fields, api

class TuniRentReport(models.Model):
    _name = 'tuni.rent.report'
    _description = 'Báo cáo chi phí thuê hàng tháng'
    _order = 'nam desc, thang desc'

    thang = fields.Selection(
        [(str(i), f'Tháng {i}') for i in range(1, 13)],
        string='Tháng',
        required=True
    )
    nam = fields.Integer(string='Năm', required=True, default=lambda self: fields.Date.today().year)

    tien_thue_mat_bang = fields.Float(string='Tiền thuê mặt bằng (VND)', required=True)
    tien_dien = fields.Float(string='Tiền điện (VND)', required=True)
    tien_nuoc = fields.Float(string='Tiền nước (VND)', required=True)

    tong_chi_phi = fields.Float(string='Tổng chi phí (VND)', compute='_compute_tong_chi_phi', store=True)

    @api.depends('tien_thue_mat_bang', 'tien_dien', 'tien_nuoc')
    def _compute_tong_chi_phi(self):
        for rec in self:
            rec.tong_chi_phi = rec.tien_thue_mat_bang + rec.tien_dien + rec.tien_nuoc

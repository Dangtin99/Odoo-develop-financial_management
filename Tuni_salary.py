from odoo import models, fields, api
from datetime import date, timedelta

class TuniSalary(models.TransientModel):
    _name = 'tuni.salary'
    _description = 'Bảng tính lương'

    khoang_thoi_gian = fields.Selection([
        ('month', 'Tháng này'),
        ('quarter', 'Quý này'),
        ('year', 'Năm nay'),
        ('date', 'Tùy chọn ngày'),
    ], string='Khoảng thời gian', required=True, default='month')

    date_from = fields.Date(string='Từ ngày')
    date_to = fields.Date(string='Đến ngày')
    nhan_vien_id = fields.Many2one('tuni.employee', string='Nhân viên (tùy chọn)')
    tong_luong = fields.Integer(string='Tổng lương (VND)', readonly=True)

    def _get_date_range(self):
        today = date.today()
        if self.khoang_thoi_gian == 'month':
            start = today.replace(day=1)
            end = today
        elif self.khoang_thoi_gian == 'quarter':
            month = (today.month - 1) // 3 * 3 + 1
            start = today.replace(month=month, day=1)
            end = today
        elif self.khoang_thoi_gian == 'year':
            start = today.replace(month=1, day=1)
            end = today
        elif self.khoang_thoi_gian == 'date':
            if not self.date_from or not self.date_to:
                raise ValueError("Bạn cần chọn Từ ngày và Đến ngày.")
            start = self.date_from
            end = self.date_to
        else:
            start = end = today
        return start, end

    def action_tinh_luong(self):
        start_date, end_date = self._get_date_range()

        domain = [('ngay_cham_cong', '>=', start_date), ('ngay_cham_cong', '<=', end_date)]
        if self.nhan_vien_id:
            domain.append(('nhan_vien_id', '=', self.nhan_vien_id.id))

        attendances = self.env['tuni.attendance'].search(domain)
        self.tong_luong = sum(att.luong_thuc_te for att in attendances)

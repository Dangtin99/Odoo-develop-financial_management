from odoo import models, fields,api

class TuniShift(models.Model):
    _name = 'tuni.attendance'
    _description = 'Chấm công'

    nhan_vien_id = fields.Many2one('tuni.employee', string='Nhân viên', required=True)
    ngay_cham_cong = fields.Date(string='Ngày bán', default=lambda self: self.env.context.get('default_ngay_cham_cong', fields.Date.today()),
    required=True)
    ca_lam = fields.Selection([
        ('morning', 'Ca sáng (7h-14h)'),
        ('afternoon', 'Ca chiều (14h-20h)'),
        ('evening', 'Ca tối (17h-23h)'),
    ], string='Ca làm')
    work = fields.Selection([
        ('yes', 'Có đi làm'),
        ('no', 'Không đi làm'),
    ], string='Trạng thái đi làm', required=True, default='yes')
    time_start = fields.Float(string='Giờ bắt đầu')
    time_end = fields.Float(string='Giờ kết thúc')
    luong_theo_gio = fields.Integer(string='Lương theo giờ (VND)', required=True)
    
    luong_thuc_te = fields.Integer(string='Lương thực tế (VND)', compute='_compute_luong_thuc_te', store=True)

    @api.depends('work', 'time_start', 'time_end', 'luong_theo_gio')
    def _compute_luong_thuc_te(self):
        for record in self:
            if record.work == 'no':
                record.time_start = 0.0
                record.time_end = 0.0
                record.luong_thuc_te = 0
            else:
                gio_lam = max(record.time_end - record.time_start, 0.0)
                record.luong_thuc_te = int(record.luong_theo_gio * gio_lam)
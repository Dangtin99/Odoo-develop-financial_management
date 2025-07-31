from odoo import models, fields
from datetime import date

class TuniAttendance(models.Model):
    _name = 'tuni.shift'
    _description = 'Phân ca làm'

    nhan_vien_id = fields.Many2one('tuni.employee', string='Nhân viên', required=True)
    phan_ca = fields.Selection([
        ('morning', 'Ca sáng (7h-14h)'),
        ('afternoon', 'Ca chiều (14h-20h)'),
        ('evening', 'Ca tối (17h-23h)'),
    ], string='Ca làm')
    ngay_lam = fields.Date(string='Ngày làm việc', default=lambda self: self.env.context.get('default_ngay_lam', fields.Date.today()),
    required=True)
    

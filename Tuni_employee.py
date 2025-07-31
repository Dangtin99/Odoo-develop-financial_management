from odoo import models, fields

class TuniEmployee(models.Model):
    _name = 'tuni.employee'
    _description = 'Quản lý nhân sự quán Tuni'

    name = fields.Char(string='Họ và tên', required=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ')
    ], string='Giới tính')

    position = fields.Selection([
        ('barista', 'Pha chế'),
        ('cashier', 'Thu ngân'),
        ('cleaner', 'Dọn dẹp'),
        ('manager', 'Quản lý'),
    ], string='Chức vụ', required=True)

    salary = fields.Integer(string='Lương cơ bản (VND)', required=True)
    phone = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    start_date = fields.Date(string='Ngày vào làm')
    ca_id = fields.Selection([
        ('morning', 'Ca sáng (7h-14h)'),
        ('afternoon', 'Ca chiều (14h-20h)'),
        ('evening', 'Ca tối (17h-23h)'),
    ], string='Ca làm')
    note = fields.Text(string='Ghi chú')

    image = fields.Binary(string='Ảnh đại diện')

from odoo import models, fields, api

class TuniMenu(models.Model):
    _name = 'tuni.menu'
    _description = 'Menu quán Tuni'

    name = fields.Char(string='Tên món', required=True)
    gia_ban = fields.Integer(string='Giá bán (VND)', required=True)
    size = fields.Selection([
        ('Size_M', 'Size M'),
        ('Size_L', 'Size L'),
    ], string='Size Ly', required=False)
    phan_khuc = fields.Selection([
        ('matcha_dai', 'Matcha Đài Loan'),
        ('matcha_uji', 'Matcha Uji'),
        ('matcha_haru', 'Matcha Haru'),
        ('ca_cao','Cacao'),
        ('khoai_mon','Khoai Môn'),
        ('Topping','Món thêm'),
        ('ca_phe', 'Cà phê'),
        ('tra', 'Trà'),
    ], string='Phân khúc món', required=True)

    milk = fields.Selection([
        ('Sua_tuoi', 'Sữa tươi'),
        ('Oatside', 'Sữa OatSide'),
        ('Gau', 'Sữa gấu'),
    ], string='Phân khúc sữa')

    @api.onchange('phan_khuc')
    def _onchange_phan_khuc(self):
        if self.phan_khuc in ['matcha_dai', 'matcha_uji', 'matcha_haru']:
            pass
        else:
            self.milk = False

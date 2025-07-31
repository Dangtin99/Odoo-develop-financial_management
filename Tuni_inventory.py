from odoo import models, fields, api

class TuniInventory(models.Model):
    _name = 'tuni.inventory'
    _description = 'Quản lý kho hàng'
    _order = 'id desc'

    ma_so_kho = fields.Char(string="Mã số kho", required=True, default=lambda self: self._generate_sequence(), copy=False)
    ten_mon_hang = fields.Char(string="Tên món hàng", required=True)
    ngay_mua = fields.Date(string='Ngày mua', required=True)
    so_luong = fields.Integer(string="Số lượng", required=True)
    tinh_trang = fields.Selection([
        ('ton_kho', 'Còn hàng'),
        ('het_hang', 'Hết hàng'),
    ], string="Tình trạng", default='ton_kho')

    @api.model
    def _generate_sequence(self):
        return self.env['ir.sequence'].next_by_code('tuni.inventory.sequence')

    @api.model
    def create_from_purchase(self, purchase_vals):
        # Chỉ tìm theo tên món hàng, không cần mã số kho
        existing_product = self.search([
            ('ten_mon_hang', '=', purchase_vals.get('ten_mon_hang'))
        ], limit=1)

        if existing_product:
            # Cập nhật số lượng và ngày mua mới nhất
            existing_product.write({
                'so_luong': existing_product.so_luong + purchase_vals.get('so_luong', 0),
                'ngay_mua': purchase_vals.get('ngay_mua', fields.Date.today()),
            })
            return existing_product
        else:
            # Tạo mới với sequence tự động
            vals = {
                'ten_mon_hang': purchase_vals.get('ten_mon_hang'),
                'ngay_mua': purchase_vals.get('ngay_mua', fields.Date.today()),
                'so_luong': purchase_vals.get('so_luong', 1),
                'tinh_trang': 'ton_kho',
            }
            return self.create(vals)

    @api.model
    def create(self, vals):
        if not vals.get('ma_so_kho'):
            vals['ma_so_kho'] = self._generate_sequence()
        return super(TuniInventory, self).create(vals)
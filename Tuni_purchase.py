from odoo import models, fields, api

class TuniPurchase(models.Model):
    _name = 'tuni.purchase'
    _description = 'Lịch sử mua hàng'

    ten_mon_hang = fields.Char(string="Tên món hàng", required=True)
    gia = fields.Float(string="Giá tiền (VND)", required=True)
    ngay_mua = fields.Date(string='Ngày mua', default=lambda self: self.env.context.get('default_ngay_mua', fields.Date.today()),
    required=True)
    so_luong = fields.Integer(string="Số lượng", required=True)
    chi_phi = fields.Float(string="Chi phí (VND)", compute='_compute_chi_phi', store=True)

    @api.depends('gia', 'so_luong')
    def _compute_chi_phi(self):
        for record in self:
            record.chi_phi = record.gia * record.so_luong

    @api.model_create_multi
    def create(self, vals_list):
        purchases = super().create(vals_list)
        inventory_model = self.env['tuni.inventory']
        
        for purchase in purchases:
            inventory_model.create_from_purchase({
                'ma_so_kho': 'KHO001',  
                'ten_mon_hang': purchase.ten_mon_hang,
                'ngay_mua': purchase.ngay_mua,
                'so_luong': purchase.so_luong,
            })
        return purchases
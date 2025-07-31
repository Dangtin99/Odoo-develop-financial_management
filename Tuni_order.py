from odoo import models, fields, api
from odoo.exceptions import UserError

class TuniOrder(models.Model):
    _name = 'tuni.order'
    _description = 'Order của từng bàn'

    name = fields.Char(string='Mã Order', required=True, default='New')
    ban_so = fields.Char(string='Bàn số', required=True)
    order_line_ids = fields.One2many('tuni.order.line', 'order_id', string='Chi tiết món gọi')
    
    trang_thai = fields.Selection([
        ('draft', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán')
    ], default='draft', string='Trạng thái')
    
    ngay_order = fields.Date(
        string='Ngày order',
        default=lambda self: self.env.context.get('default_ngay_order', fields.Date.today()),
    required=True)

    tong_tien = fields.Integer(string='Tổng tiền', compute='_compute_tong_tien', store=True)

    @api.depends('order_line_ids.thanh_tien')
    def _compute_tong_tien(self):
        for order in self:
            order.tong_tien = sum(line.thanh_tien for line in order.order_line_ids)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('tuni.order') or 'New'
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        if 'trang_thai' in vals and vals['trang_thai'] == 'paid':
            TuniSale = self.env['tuni.sale']
            for order in self:
                for line in order.order_line_ids:
                # Tìm bản ghi đã có sẵn
                    existing_sale = TuniSale.search([
                        ('menu_item_id', '=', line.menu_item_id.id),
                        ('size', '=', line.size),
                        ('ngay_ban', '=', order.ngay_order),
                    ], limit=1)

                    if existing_sale:
                    # Cộng dồn số lượng và doanh thu
                        existing_sale.so_luong += line.so_luong
                        existing_sale.doanh_thu += line.thanh_tien
                    else:
                    # Tạo mới nếu chưa có
                        TuniSale.create({
                            'menu_item_id': line.menu_item_id.id,
                            'size': line.size,
                            'so_luong': line.so_luong,
                            'ngay_ban': order.ngay_order,
                            'doanh_thu': line.thanh_tien
                    })
        return res

from odoo import models, fields, api
class TuniOrderLine(models.Model):
    _name = 'tuni.order.line'
    _description = 'Chi tiết món trong order'

    order_id = fields.Many2one('tuni.order', string='Order')
    menu_item_id = fields.Many2one('tuni.menu', string='Món')
    size = fields.Selection([
        ('Size_M', 'Size M'),
        ('Size_L', 'Size L')
    ], string='Size', required=True)
    so_luong = fields.Integer(string='Số lượng', default=1)
    don_gia = fields.Integer(string='Đơn giá', compute='_compute_don_gia', store=True)
    thanh_tien = fields.Integer(string='Thành tiền', compute='_compute_thanh_tien', store=True)

    @api.depends('menu_item_id', 'size')
    def _compute_don_gia(self):
        for rec in self:
            price = self.env['tuni.menu'].search([
                ('name', '=', rec.menu_item_id.name),
                ('size', '=', rec.size) 
            ], limit=1)
            rec.don_gia = price.gia_ban if price else 0

    @api.depends('don_gia', 'so_luong')
    def _compute_thanh_tien(self):
        for rec in self:
            rec.thanh_tien = rec.don_gia * rec.so_luong

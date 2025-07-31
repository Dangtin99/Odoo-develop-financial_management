from importlib.metadata import requires
from odoo import models, fields, api

class TuniSale(models.Model):
    _name = 'tuni.sale'
    _description = 'Giao dịch bán hàng trong ngày'

    menu_item_id = fields.Many2one('tuni.menu', string='Món đã bán', required=True)
    size = fields.Selection([
        ('Size_M', 'Size M'),
        ('Size_L', 'Size L'),
    ], string='Size Ly')
    so_luong = fields.Integer(string='Số lượng', default=1, required=True)
    ngay_ban = fields.Date(
    string='Ngày bán',
    default=lambda self: self.env.context.get('default_ngay_ban', fields.Date.today()),
    required=True)

    doanh_thu = fields.Integer(string='Doanh thu', compute='_compute_tinh_tien', store=True)

    @api.depends('menu_item_id', 'size', 'so_luong')
    def _compute_tinh_tien(self):
        for rec in self:
            menu = self.env['tuni.menu'].search([
                ('name', '=', rec.menu_item_id.name),
                ('size', '=', rec.size)
            ], limit=1)
            if menu:
                rec.doanh_thu = rec.so_luong * menu.gia_ban
               
            else:
                rec.doanh_thu = 0
               

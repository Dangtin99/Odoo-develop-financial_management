from odoo import models, fields, api

class TuniCustomer(models.Model):
    _name = 'tuni.customer'
    _description = 'Khách hàng'
    _order = 'id'

    card_number = fields.Char(string='Số thẻ khách hàng', readonly=True, copy=False, default='New')
    name = fields.Char(string='Tên khách hàng', required=True)
    phone = fields.Char(string='Số điện thoại')
    birthday = fields.Date(string='Ngày sinh')

    @api.model
    def create(self, vals):
        if vals.get('card_number', 'New') == 'New':
            vals['card_number'] = self.env['ir.sequence'].next_by_code('tuni.customer.seq') or 'KH0001'
        return super().create(vals)

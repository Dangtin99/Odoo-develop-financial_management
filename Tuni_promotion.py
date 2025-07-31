from odoo import models, fields, api
from datetime import date

class TuniPromotion(models.Model):
    _name = 'tuni.promotion'
    _description = 'Ưu đãi'

    code = fields.Char(string='Mã ưu đãi', required=True)
    value = fields.Float(string='Giá trị (%)')
    condition = fields.Text(string='Điều kiện áp dụng')
    start_date = fields.Date(string='Thời gian bắt đầu')
    end_date = fields.Date(string='Thời gian kết thúc')

    @api.model
    def delete_expired_promotions(self):
        expired_promos = self.search([('end_date', '<', date.today())])
        expired_promos.unlink()

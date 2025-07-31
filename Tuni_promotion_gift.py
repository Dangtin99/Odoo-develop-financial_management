from venv import logger
from odoo import models, fields, api
from datetime import date

class TuniPromotionGift(models.Model):
    _name = 'tuni.promotion.gift'
    _description = 'Gửi ưu đãi sinh nhật'

    @api.model
    def send_birthday_gifts(self):
        today = date.today()
        customers = self.env['tuni.customer'].search([])

        for customer in customers:
            if customer.birthday and customer.birthday.month == today.month and customer.birthday.day == today.day:
                # Tạo mã khuyến mãi cá nhân
                promo_code = f"FREE-{customer.card_number}"
                self.env['tuni.promotion'].create({
                    'code': promo_code,
                    'value': 100,
                    'condition': 'Áp dụng cho 1 ly nước bất kỳ',
                    'start_date': today,
                    'end_date': today,
                })
                # Gửi thông báo/sms (ở đây giả lập)
                logger.info(f"Gửi mã {promo_code} đến {customer.phone}")

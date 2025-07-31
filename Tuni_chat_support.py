from odoo import models, fields

class TuniChatSupport(models.Model):  # kế thừa từ models.Model
    _name = 'tuni.chat.support'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # kế thừa chức năng
    _description = 'Chat hỗ trợ khách hàng'

    name =fields.Char(string="Tiêu đề", tracking=True)
    customer_id = fields.Char(string="Tên người gửi", tracking=True)
    message = fields.Text(string="Nội dung", tracking=True)

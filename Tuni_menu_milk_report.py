from odoo import models, fields, api
from datetime import datetime, timedelta
import calendar

class TuniMenuSegmentReport(models.Model):
    _name = 'tuni.menu.milk.report'
    _description = 'Báo cáo tỷ lệ bán theo dòng sữa (Matcha Only)'

    name = fields.Char(string="Tên báo cáo", default="Báo cáo doanh thu theo dòng sữa")
    time_range = fields.Selection([
        ('day', 'Ngày'),
        ('week', 'Tuần'),
        ('month', 'Tháng'),
        ('quarter', 'Quý'),
        ('year', 'Năm')
    ], string="Khoảng thời gian", default='month')
    date_from = fields.Date(string="Từ ngày")
    date_to = fields.Date(string="Đến ngày")

    milk_id = fields.Selection([
        ('Sua_tuoi', 'Sữa tươi'),
        ('Oatside', 'Sữa OatSide'),
        ('Gau', 'Sữa gấu'),
    ], string='Phân khúc sữa', required=True)

    so_luong = fields.Integer(string='Tổng số lượng đã bán', compute='_compute_data', store=True)
    doanh_thu = fields.Integer(string='Tổng doanh thu (VND)', compute='_compute_data', store=True)
    loi_nhuan = fields.Integer(string='Tổng lợi nhuận (VND)', compute='_compute_data', store=True)

    phan_tram_so_luong = fields.Float(string='Tỷ lệ % số lượng', compute='_compute_percentages', store=True)
    phan_tram_doanh_thu = fields.Float(string='Tỷ lệ % doanh thu', compute='_compute_percentages', store=True)

    @api.onchange('time_range')
    def _onchange_time_range(self):
        today = fields.Date.today()
        if self.time_range == 'day':
            self.date_from = today
            self.date_to = today
        elif self.time_range == 'week':
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            self.date_from = start
            self.date_to = end
        elif self.time_range == 'month':
            start = today.replace(day=1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            end = today.replace(day=last_day)
            self.date_from = start
            self.date_to = end
        elif self.time_range == 'quarter':
            current_quarter = (today.month - 1) // 3 + 1
            start_month = 3 * (current_quarter - 1) + 1
            start = datetime(today.year, start_month, 1).date()
            end_month = start_month + 2
            last_day = calendar.monthrange(today.year, end_month)[1]
            end = datetime(today.year, end_month, last_day).date()
            self.date_from = start
            self.date_to = end
        elif self.time_range == 'year':
            self.date_from = datetime(today.year, 1, 1).date()
            self.date_to = datetime(today.year, 12, 31).date()

    @api.depends('milk_id', 'date_from', 'date_to')
    def _compute_data(self):
        for record in self:
            sale_obj = self.env['tuni.sale']
            menu_obj = self.env['tuni.menu']

            # Tìm món Matcha có milk đúng phân khúc
            menu_ids = menu_obj.search([
                ('milk', '=', record.milk_id),
                ('phan_khuc', 'in', ['matcha_dai', 'matcha_uji', 'matcha_haru'])
            ]).ids

            domain = [('menu_item_id', 'in', menu_ids)]
            if record.date_from and record.date_to:
                domain += [('create_date', '>=', record.date_from), ('create_date', '<=', record.date_to)]

            related_sales = sale_obj.search(domain)

            record.so_luong = sum(sale.so_luong for sale in related_sales)
            record.doanh_thu = sum(sale.doanh_thu for sale in related_sales)
    @api.depends('so_luong', 'doanh_thu', 'time_range', 'date_from', 'date_to')
    def _compute_percentages(self):
        for record in self:
            sale_obj = self.env['tuni.sale']
            menu_obj = self.env['tuni.menu']

            # Lấy tất cả món Matcha trong khoảng thời gian
            matcha_menu_ids = menu_obj.search([
                ('phan_khuc', 'in', ['matcha_dai', 'matcha_uji', 'matcha_haru'])
            ]).ids

            domain = [('menu_item_id', 'in', matcha_menu_ids)]
            if record.date_from and record.date_to:
                domain += [('create_date', '>=', record.date_from), ('create_date', '<=', record.date_to)]

            all_sales = sale_obj.search(domain)

            tong_so_luong = sum(sale.so_luong for sale in all_sales)
            tong_doanh_thu = sum(sale.doanh_thu for sale in all_sales)

            record.phan_tram_so_luong = (record.so_luong / tong_so_luong * 100) if tong_so_luong else 0
            record.phan_tram_doanh_thu = (record.doanh_thu / tong_doanh_thu * 100) if tong_doanh_thu else 0

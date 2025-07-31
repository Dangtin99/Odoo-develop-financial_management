from odoo import models, fields, api
from datetime import date, timedelta

class TuniFinance(models.TransientModel):
    _name = 'tuni.finance'
    _description = 'Thống kê tài chính trong ngày'

    khoang_thoi_gian = fields.Selection([
        ('date', 'Tùy chọn ngày'),
        ('week', 'Tuần này'),
        ('month', 'Tháng này'),
        ('quarter', 'Quý này'),
        ('year', 'Năm nay'),
    ], string='Khoảng thời gian', required=True, default='date')

    date_from = fields.Date(string='Từ ngày')
    date_to = fields.Date(string='Đến ngày')
    menu_item_id = fields.Many2one('tuni.menu', string='Món bán')
    phan_khuc = fields.Integer(string='Số lượng')

    tong_so_ly = fields.Integer(string='Tổng số ly đã bán', readonly=True)
    tong_doanh_thu = fields.Integer(string='Tổng doanh thu (VND)', readonly=True)
    tong_chi_phi = fields.Integer(string='Tổng chi phí (VND)', readonly=True)
    tong_loi_nhuan = fields.Integer(string='Tổng lợi nhuận (VND)', readonly=True)
    moc_tai_chinh = fields.Char(string='Mốc tài chính đã đạt', readonly=True)

    tien_thue_mat_bang = fields.Integer(string='Tiền thuê mặt bằng (VND)', readonly=True)
    tien_dien = fields.Integer(string='Tiền điện (VND)', readonly=True)
    tien_nuoc = fields.Integer(string='Tiền nước (VND)', readonly=True)

    hien_thi_chi_phi = fields.Boolean(string='Hiển thị chi phí', compute='_compute_hien_thi_chi_phi', store=False)

    @api.depends('khoang_thoi_gian')
    def _compute_hien_thi_chi_phi(self):
        for record in self:
            record.hien_thi_chi_phi = record.khoang_thoi_gian != 'week'

    def action_tinh_toan(self):
        today = date.today()

        # Xác định start_date và end_date dựa vào lựa chọn
        if self.khoang_thoi_gian == 'date':
            if not self.date_from or not self.date_to:
                raise ValueError("Bạn cần chọn 'Từ ngày' và 'Đến ngày' khi chọn tùy chọn ngày.")
            start_date = self.date_from
            end_date = self.date_to
        else:
            end_date = today
            if self.khoang_thoi_gian == 'week':
                start_date = today - timedelta(days=today.weekday())
            elif self.khoang_thoi_gian == 'month':
                start_date = today.replace(day=1)
            elif self.khoang_thoi_gian == 'quarter':
                month = (today.month - 1) // 3 * 3 + 1
                start_date = today.replace(month=month, day=1)
            elif self.khoang_thoi_gian == 'year':
                start_date = today.replace(month=1, day=1)
            else:
                start_date = today

        # Truy vấn dữ liệu bán hàng
        sales = self.env['tuni.sale'].search([
            ('ngay_ban', '>=', start_date),
            ('ngay_ban', '<=', end_date)
        ])
        tong_so_ly = 0
        for s in sales:
            if s.menu_item_id and s.menu_item_id.phan_khuc != 'Topping':
                tong_so_ly += s.so_luong
        self.tong_so_ly = tong_so_ly
        self.tong_doanh_thu = sum(sales.mapped('doanh_thu'))

        # Truy vấn chi phí nhập hàng
        purchases = self.env['tuni.purchase'].search([
            ('ngay_mua', '>=', start_date),
            ('ngay_mua', '<=', end_date)
        ])
        self.tong_chi_phi = sum(purchases.mapped('chi_phi'))

        # Truy vấn chi phí thuê mặt bằng, điện, nước
        self.tien_thue_mat_bang = 0
        self.tien_dien = 0
        self.tien_nuoc = 0

        if self.khoang_thoi_gian != 'week':
            if self.khoang_thoi_gian == 'date':
                # Lấy danh sách các tháng và năm trong khoảng từ start_date đến end_date
                current = start_date.replace(day=1)
                end_month = end_date.replace(day=1)
                months = []
                while current <= end_month:
                    months.append((current.month, current.year))
                    if current.month == 12:
                        current = current.replace(year=current.year + 1, month=1)
                    else:
                        current = current.replace(month=current.month + 1)
                domain = [('thang', 'in', [m[0] for m in months]), ('nam', 'in', [m[1] for m in months])]
            else:
                domain = [('nam', '=', today.year)]
                if self.khoang_thoi_gian == 'month':
                    domain.append(('thang', '=', today.month))
                elif self.khoang_thoi_gian == 'quarter':
                    quarter_months = {
                        1: [1, 2, 3],
                        2: [4, 5, 6],
                        3: [7, 8, 9],
                        4: [10, 11, 12],
                    }
                    quarter = (today.month - 1) // 3 + 1
                    domain.append(('thang', 'in', quarter_months[quarter]))

            rents = self.env['tuni.rent.report'].search(domain)
            self.tien_thue_mat_bang = sum(rents.mapped('tien_thue_mat_bang'))
            self.tien_dien = sum(rents.mapped('tien_dien'))
            self.tien_nuoc = sum(rents.mapped('tien_nuoc'))

        # Tính lợi nhuận
        self.tong_loi_nhuan = self.tong_doanh_thu - self.tong_chi_phi \
                              - self.tien_thue_mat_bang - self.tien_dien - self.tien_nuoc

        # Mốc tài chính tích lũy
        all_sales = self.env['tuni.sale'].search([('ngay_ban', '<=', today)])
        all_purchases = self.env['tuni.purchase'].search([('ngay_mua', '<=', today)])
        all_doanh_thu = sum(all_sales.mapped('doanh_thu'))
        all_chi_phi = sum(all_purchases.mapped('chi_phi'))
        loi_nhuan_tich_luy = all_doanh_thu - all_chi_phi

        mốc = int(loi_nhuan_tich_luy / 10000000) * 10
        if mốc > 0:
            self.moc_tai_chinh = f"🎉 Đạt mốc {mốc} triệu lợi nhuận tích lũy!"
        else:
            self.moc_tai_chinh = "Chưa đạt mốc tài chính nào."

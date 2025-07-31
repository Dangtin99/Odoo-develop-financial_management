# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TuniChart(models.TransientModel):
    _name = 'tuni.chart'
    _description = 'Revenue and Profit Chart Report'
    

    report_type = fields.Selection([
        ('month', 'Monthly'),
        ('quarter', 'Quarterly'),
        ('year', 'Yearly'),
    ], string='Report Type', default='month', required=True)
    
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month')
    
    quarter = fields.Selection([
        ('1', 'Q1 (Jan-Mar)'),
        ('2', 'Q2 (Apr-Jun)'),
        ('3', 'Q3 (Jul-Sep)'),
        ('4', 'Q4 (Oct-Dec)'),
    ], string='Quarter')
    
    year = fields.Integer(string='Year', default=fields.Date.today().year, required=True)

    @api.onchange('report_type')
    def _onchange_report_type(self):
        """Clear month/quarter when changing report type"""
        if self.report_type:
            self.month = False
            self.quarter = False

    def _get_date_range(self):
        """Calculate date range based on report parameters"""
        self.ensure_one()
        
        if self.report_type == 'month' and self.month:
            date_from = datetime(self.year, int(self.month), 1).date()
            date_to = date_from + relativedelta(months=1, days=-1)
        elif self.report_type == 'quarter' and self.quarter:
            quarter = int(self.quarter)
            month_from = (quarter - 1) * 3 + 1
            date_from = datetime(self.year, month_from, 1).date()
            date_to = date_from + relativedelta(months=3, days=-1)
        else:  # yearly
            date_from = datetime(self.year, 1, 1).date()
            date_to = datetime(self.year, 12, 31).date()
        
        return date_from, date_to

    def _get_chart_data(self):
        """Prepare data for chart"""
        self.ensure_one()
        date_from, date_to = self._get_date_range()
        
        # Get revenue from sales
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
            ('state', 'in', ['sale', 'done'])
        ])
        revenue = sum(order.amount_total for order in sale_orders)
        
        # Get costs from purchases
        purchase_orders = self.env['purchase.order'].search([
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
            ('state', 'in', ['purchase', 'done'])
        ])
        cost = sum(order.amount_total for order in purchase_orders)
        
        profit = revenue - cost
        
        return {
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'date_from': date_from,
            'date_to': date_to,
        }

    def get_bar_chart_config(self):
        """Return configuration for bar chart"""
        data = self._get_chart_data()
        
        return {
            'type': 'bar',
            'data': {
                'labels': ['Doanh thu', 'Chi phí', 'Lợi nhuận'],
                'datasets': [{
                    'label': 'Số tiền',
                    'data': [data['revenue'], data['cost'], data['profit']],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.5)',  # Blue for revenue
                        'rgba(255, 99, 132, 0.5)',  # Red for cost
                        'rgba(75, 192, 192, 0.5)',  # Green for profit
                    ],
                    'borderColor': [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)',
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': f'Báo cáo {self.report_type} {self.year}'
                    },
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'title': {
                            'display': True,
                            'text': 'Số tiền'
                        }
                    }
                }
            }
        }

    def action_view_chart(self):
        """Action to display the chart"""
        self.ensure_one()
        
        if self.report_type == 'month' and not self.month:
            raise models.ValidationError("Vui lòng chọn tháng cho báo cáo hàng tháng")
        if self.report_type == 'quarter' and not self.quarter:
            raise models.ValidationError("Vui lòng chọn quý cho báo cáo hàng quý")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'tuni_chart_view',
            'name': 'Biểu đồ Doanh thu và Lợi nhuận',
            'context': {
                'chart_config': self.get_bar_chart_config(),
                'report_type': self.report_type,
                'period': self.month or self.quarter or str(self.year),
                'year': self.year,
            }
        }
    
    def action_open_chart(self):
        """Mở view biểu đồ JavaScript từ Python"""
        self.ensure_one()  # Đảm bảo chỉ làm việc với 1 record
    
    # Lấy dữ liệu biểu đồ
        chart_data = self._get_chart_data()
    
        return {
            'type': 'ir.actions.client',
            'tag': 'tuni_chart_action',  # Phải trùng với tên đã đăng ký trong JS
            'name': 'Biểu đồ Doanh thu & Lợi nhuận',
            'params': {  # Dữ liệu truyền sang JS
             'chart_config': self.get_bar_chart_config(),
            'report_type': self.report_type,
            'period': self.month or self.quarter or str(self.year),
            },
            'target': 'new',  # Mở trong cửa sổ mới
        }
import tkinter as tk
from tkinter import ttk
import db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Metrics
        metrics_frame = tk.Frame(self)
        metrics_frame.pack(fill='x', padx=10, pady=5)
        total_today = db.get_total_sales_today()
        total_month = db.get_total_sales_month()
        tk.Label(metrics_frame, text=f'Total Sales Today: ₹{total_today:.2f}').pack(side='left', padx=10)
        tk.Label(metrics_frame, text=f'Total Sales This Month: ₹{total_month:.2f}').pack(side='left', padx=10)

        # Top Products
        top_frame = tk.LabelFrame(self, text='Top 5 Best-Selling Products')
        top_frame.pack(fill='x', padx=10, pady=5)
        top_products = db.get_top_products()
        for i, (name, qty) in enumerate(top_products, 1):
            tk.Label(top_frame, text=f'{i}. {name} ({qty} sold)').pack(anchor='w')

        # Low Stock
        low_stock_frame = tk.LabelFrame(self, text='Products with Low Stock (<5)')
        low_stock_frame.pack(fill='x', padx=10, pady=5)
        low_stock = db.get_low_stock_products()
        for prod in low_stock:
            tk.Label(low_stock_frame, text=f'{prod[1]} (Stock: {prod[4]})').pack(anchor='w')

        # Charts
        chart_frame = tk.Frame(self)
        chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.create_charts(chart_frame)

    def create_charts(self, parent):
        # Bar chart: Sales per product
        sales_data = db.get_sales_per_product()
        names = [x[0] for x in sales_data]
        sales = [x[1] for x in sales_data]
        fig, axs = plt.subplots(1, 2, figsize=(8, 3))
        axs[0].bar(names, sales)
        axs[0].set_title('Sales per Product')
        axs[0].set_ylabel('Total Sales (₹)')
        axs[0].tick_params(axis='x', rotation=45)
        # Pie chart: Sales by category
        cat_data = db.get_sales_by_category()
        cat_names = [x[0] for x in cat_data]
        cat_sales = [x[1] for x in cat_data]
        axs[1].pie(cat_sales, labels=cat_names, autopct='%1.1f%%')
        axs[1].set_title('Sales by Category')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True) 
import tkinter as tk
from tkinter import ttk, messagebox
import db
from utils import is_non_empty
from datetime import datetime

class SalesGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text='New Sale')
        form_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(form_frame, text='Customer').grid(row=0, column=0)
        tk.Label(form_frame, text='Product').grid(row=0, column=2)
        tk.Label(form_frame, text='Quantity').grid(row=1, column=0)
        self.customer_var = tk.StringVar()
        self.product_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.customers = db.get_customers()
        self.products = db.get_products()
        customer_names = [f"{c[0]} - {c[1]}" for c in self.customers]
        product_names = [f"{p[0]} - {p[1]}" for p in self.products]
        self.customer_cb = ttk.Combobox(form_frame, textvariable=self.customer_var, values=customer_names, state='readonly')
        self.product_cb = ttk.Combobox(form_frame, textvariable=self.product_var, values=product_names, state='readonly')
        self.customer_cb.grid(row=0, column=1)
        self.product_cb.grid(row=0, column=3)
        tk.Entry(form_frame, textvariable=self.quantity_var).grid(row=1, column=1)
        tk.Button(form_frame, text='Add Sale', command=self.add_sale).grid(row=1, column=3)

        self.tree = ttk.Treeview(self, columns=('ID', 'Date', 'Customer', 'Product', 'Qty', 'Total', 'Paid'), show='headings')
        for col in ('ID', 'Date', 'Customer', 'Product', 'Qty', 'Total', 'Paid'):
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

    def load_sales(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        sales = db.get_sales()
        customers = {c[0]: c[1] for c in db.get_customers()}
        products = {p[0]: p[1] for p in db.get_products()}
        for sale in sales:
            sale_id, date, cust_id, prod_id, qty, total, paid = sale
            cust_name = customers.get(cust_id, '')
            prod_name = products.get(prod_id, '')
            self.tree.insert('', 'end', values=(sale_id, date, cust_name, prod_name, qty, total, 'Yes' if paid else 'No'))

    def add_sale(self):
        cust_val = self.customer_var.get()
        prod_val = self.product_var.get()
        qty = self.quantity_var.get()
        if not (cust_val and prod_val and qty.isdigit() and int(qty) > 0):
            messagebox.showerror('Error', 'Please enter valid sale details.')
            return
        cust_id = int(cust_val.split(' - ')[0])
        prod_id = int(prod_val.split(' - ')[0])
        product = next((p for p in self.products if p[0] == prod_id), None)
        if not product:
            messagebox.showerror('Error', 'Product not found.')
            return
        price = product[3]
        total_price = price * int(qty)
        date = datetime.now().strftime('%Y-%m-%d')
        success = db.add_sale(date, cust_id, prod_id, int(qty), total_price)
        if not success:
            messagebox.showerror('Error', 'Not enough stock.')
            return
        self.load_sales()
        self.quantity_var.set('')
        self.products = db.get_products()
        self.product_cb['values'] = [f"{p[0]} - {p[1]}" for p in self.products]
        messagebox.showinfo('Success', 'Sale added successfully.') 
import tkinter as tk
from tkinter import ttk, messagebox
import db
from utils import is_non_empty, is_positive_number

class ProductGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_products()
        self.show_low_stock_alert()

    def create_widgets(self):
        # Form
        form_frame = tk.LabelFrame(self, text='Product Details')
        form_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(form_frame, text='Name').grid(row=0, column=0)
        tk.Label(form_frame, text='Category').grid(row=0, column=2)
        tk.Label(form_frame, text='Price').grid(row=1, column=0)
        tk.Label(form_frame, text='Stock Qty').grid(row=1, column=2)
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(form_frame, textvariable=self.category_var).grid(row=0, column=3)
        tk.Entry(form_frame, textvariable=self.price_var).grid(row=1, column=1)
        tk.Entry(form_frame, textvariable=self.stock_var).grid(row=1, column=3)
        tk.Button(form_frame, text='Add', command=self.add_product).grid(row=2, column=0, pady=5)
        tk.Button(form_frame, text='Update', command=self.update_product).grid(row=2, column=1)
        tk.Button(form_frame, text='Delete', command=self.delete_product).grid(row=2, column=2)
        tk.Button(form_frame, text='Clear', command=self.clear_form).grid(row=2, column=3)

        # Table
        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Category', 'Price', 'Stock'), show='headings')
        for col in ('ID', 'Name', 'Category', 'Price', 'Stock'):
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for prod in db.get_products():
            self.tree.insert('', 'end', values=prod)

    def add_product(self):
        name = self.name_var.get()
        category = self.category_var.get()
        price = self.price_var.get()
        stock = self.stock_var.get()
        if not (is_non_empty(name) and is_non_empty(category) and is_positive_number(price) and stock.isdigit()):
            messagebox.showerror('Error', 'Please enter valid product details.')
            return
        db.add_product(name, category, float(price), int(stock))
        self.load_products()
        self.clear_form()
        self.show_low_stock_alert()

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a product to update.')
            return
        prod_id = self.tree.item(selected[0])['values'][0]
        name = self.name_var.get()
        category = self.category_var.get()
        price = self.price_var.get()
        stock = self.stock_var.get()
        if not (is_non_empty(name) and is_non_empty(category) and is_positive_number(price) and stock.isdigit()):
            messagebox.showerror('Error', 'Please enter valid product details.')
            return
        db.update_product(prod_id, name, category, float(price), int(stock))
        self.load_products()
        self.clear_form()
        self.show_low_stock_alert()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a product to delete.')
            return
        prod_id = self.tree.item(selected[0])['values'][0]
        db.delete_product(prod_id)
        self.load_products()
        self.clear_form()
        self.show_low_stock_alert()

    def clear_form(self):
        self.name_var.set('')
        self.category_var.set('')
        self.price_var.set('')
        self.stock_var.set('')
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_var.set(values[1])
            self.category_var.set(values[2])
            self.price_var.set(values[3])
            self.stock_var.set(values[4])

    def show_low_stock_alert(self):
        low_stock = db.get_low_stock_products()
        if low_stock:
            msg = 'Low stock for: ' + ', '.join([p[1] for p in low_stock])
            messagebox.showwarning('Low Stock Alert', msg) 
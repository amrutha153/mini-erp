import tkinter as tk
from tkinter import ttk, messagebox
import db
from utils import is_non_empty, is_valid_email, is_valid_phone

class CustomerGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_customers()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text='Customer Details')
        form_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(form_frame, text='Name').grid(row=0, column=0)
        tk.Label(form_frame, text='Phone').grid(row=0, column=2)
        tk.Label(form_frame, text='Email').grid(row=1, column=0)
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(form_frame, textvariable=self.phone_var).grid(row=0, column=3)
        tk.Entry(form_frame, textvariable=self.email_var).grid(row=1, column=1)
        tk.Button(form_frame, text='Add', command=self.add_customer).grid(row=2, column=0, pady=5)
        tk.Button(form_frame, text='Update', command=self.update_customer).grid(row=2, column=1)
        tk.Button(form_frame, text='Delete', command=self.delete_customer).grid(row=2, column=2)
        tk.Button(form_frame, text='Clear', command=self.clear_form).grid(row=2, column=3)

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Phone', 'Email'), show='headings')
        for col in ('ID', 'Name', 'Phone', 'Email'):
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def load_customers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for cust in db.get_customers():
            self.tree.insert('', 'end', values=cust)

    def add_customer(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        if not (is_non_empty(name) and is_valid_phone(phone) and is_valid_email(email)):
            messagebox.showerror('Error', 'Please enter valid customer details.')
            return
        db.add_customer(name, phone, email)
        self.load_customers()
        self.clear_form()

    def update_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a customer to update.')
            return
        cust_id = self.tree.item(selected[0])['values'][0]
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        if not (is_non_empty(name) and is_valid_phone(phone) and is_valid_email(email)):
            messagebox.showerror('Error', 'Please enter valid customer details.')
            return
        db.update_customer(cust_id, name, phone, email)
        self.load_customers()
        self.clear_form()

    def delete_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a customer to delete.')
            return
        cust_id = self.tree.item(selected[0])['values'][0]
        db.delete_customer(cust_id)
        self.load_customers()
        self.clear_form()

    def clear_form(self):
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_var.set(values[1])
            self.phone_var.set(values[2])
            self.email_var.set(values[3]) 
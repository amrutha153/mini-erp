import tkinter as tk
from tkinter import messagebox
import db

# Import GUI modules (to be created)
# from gui.product_gui import ProductGUI
# from gui.customer_gui import CustomerGUI
# from gui.sales_gui import SalesGUI
# from gui.dashboard_gui import DashboardGUI

class MiniERPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mini ERP for Sales Management')
        self.geometry('900x600')
        self.resizable(False, False)
        self.create_menu()
        self.show_dashboard()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        module_menu = tk.Menu(menubar, tearoff=0)
        module_menu.add_command(label='Dashboard', command=self.show_dashboard)
        module_menu.add_command(label='Products', command=self.show_products)
        module_menu.add_command(label='Customers', command=self.show_customers)
        module_menu.add_command(label='Sales', command=self.show_sales)
        menubar.add_cascade(label='Modules', menu=module_menu)
        menubar.add_command(label='Exit', command=self.quit)

    def clear_frame(self):
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

    def show_dashboard(self):
        self.clear_frame()
        from gui.dashboard_gui import DashboardGUI
        DashboardGUI(self)

    def show_products(self):
        self.clear_frame()
        from gui.product_gui import ProductGUI
        ProductGUI(self)

    def show_customers(self):
        self.clear_frame()
        from gui.customer_gui import CustomerGUI
        CustomerGUI(self)

    def show_sales(self):
        self.clear_frame()
        from gui.sales_gui import SalesGUI
        SalesGUI(self)

if __name__ == '__main__':
    db.init_db()
    db.seed_example_data()
    app = MiniERPApp()
    app.mainloop() 
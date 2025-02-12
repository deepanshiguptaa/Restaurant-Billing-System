import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import ttkbootstrap as tb  

# Database Connection
db = mysql.connector.connect(host="localhost", user="root", password="khushi01", database="restaurant")
cursor = db.cursor()

# Global Variables
order_list = []

# Menu Items
menu = {
    "Burger": 50,
    "Pizza": 110,
    "Pasta": 80,
    "Coffee": 60,
    "Juice": 30
}

# Function to Add Item to Order
def add_to_order():
    item = item_var.get()
    quantity = int(quantity_var.get())

    if item and quantity > 0:
        price = menu[item]
        total_price = price * quantity
        order_list.append({"item": item, "quantity": quantity, "price": price, "total": total_price})
        update_order_display()
    else:
        messagebox.showerror("Input Error", "Please select an item and enter a valid quantity.")

# Function to Update Order Display
def update_order_display():
    for row in order_tree.get_children():
        order_tree.delete(row)
    
    for order in order_list:
        order_tree.insert("", "end", values=(order["item"], order["quantity"], f"Rs.{order['total']:.2f}"))

# Function to Calculate Total
def calculate_total():
    subtotal = sum(order["total"] for order in order_list)
    tax = subtotal * 0.05  # 5% tax
    total = subtotal + tax
    total_label.config(text=f"Total: Rs.{total:.2f}")
    return subtotal, tax, total

# Function to Generate Receipt
def generate_receipt():
    subtotal, tax, total = calculate_total()

    receipt_text = "------ Restaurant XYZ ------\n"
    for order in order_list:
        receipt_text += f"{order['item']} x{order['quantity']} - Rs.{order['total']:.2f}\n"
    
    receipt_text += f"\nSubtotal: Rs.{subtotal:.2f}\n"
    receipt_text += f"Tax (5%): Rs.{tax:.2f}\n"
    receipt_text += f"Total: Rs.{total:.2f}\n"
    receipt_text += "---------------------------\nThank You! Visit Again!\n"

    messagebox.showinfo("Receipt", receipt_text)
    save_to_database(order_list, total)

# Function to Save Order to Database
def save_to_database(order_list, total):
    for order in order_list:
        query = "INSERT INTO orders (item_name, quantity, price, total_price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (order["item"], order["quantity"], order["price"], order["total"]))
    db.commit()
    messagebox.showinfo("Order Saved", "Order successfully saved to database.")
    reset_order()

# Function to Reset Order
def reset_order():
    global order_list
    order_list = []
    for row in order_tree.get_children():
        order_tree.delete(row)
    total_label.config(text="Total: Rs.0.00")

# Create Main Window
root = tb.Window(themename="superhero")  # Apply a modern theme
root.title("Restaurant Billing System")
root.geometry("500x600")
root.resizable(False, False)

# Title Label
tb.Label(root, text="Restaurant Billing System", font=("Arial", 16, "bold")).pack(pady=10)

# Order Entry Frame
frame = tb.Frame(root, padding=10)
frame.pack(pady=5)

# Item Selection
tb.Label(frame, text="Select Item:").grid(row=0, column=0, padx=5, pady=5)
item_var = tk.StringVar(value=list(menu.keys())[0])
item_menu = tb.Combobox(frame, textvariable=item_var, values=list(menu.keys()), state="readonly")
item_menu.grid(row=0, column=1, padx=5, pady=5)

# Quantity Selection
tb.Label(frame, text="Enter Quantity:").grid(row=1, column=0, padx=5, pady=5)
quantity_var = tk.StringVar(value="1")
tb.Entry(frame, textvariable=quantity_var, width=5).grid(row=1, column=1, padx=5, pady=5)

# Add to Order Button
tb.Button(frame, text="Add to Order", command=add_to_order, bootstyle="success").grid(row=2, column=0, columnspan=2, pady=10)

# Order Summary Label
tb.Label(root, text="Order Summary:", font=("Arial", 12, "bold")).pack()

# Order Treeview Table
columns = ("Item", "Quantity", "Total Price")
order_tree = ttk.Treeview(root, columns=columns, show="headings")
order_tree.heading("Item", text="Item")
order_tree.heading("Quantity", text="Quantity")
order_tree.heading("Total Price", text="Total Price")
order_tree.pack(pady=5)

# Total Label
total_label = tb.Label(root, text="Total: Rs.0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=5)

# Buttons
btn_frame = tb.Frame(root)
btn_frame.pack(pady=10)

tb.Button(btn_frame, text="Calculate Total", command=calculate_total, bootstyle="primary").grid(row=0, column=0, padx=5)
tb.Button(btn_frame, text="Generate Receipt", command=generate_receipt, bootstyle="warning").grid(row=0, column=1, padx=5)
tb.Button(btn_frame, text="Reset", command=reset_order, bootstyle="danger").grid(row=0, column=2, padx=5)

# Run the Application
root.mainloop()

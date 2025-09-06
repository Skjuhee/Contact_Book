import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import csv

# Database Setup
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT
)
""")
conn.commit()

# Functions
def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    
    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and Phone are required!")
        return
    
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    messagebox.showinfo("Success", "Contact Added Successfully")
    clear_entries()
    view_contacts()

def view_contacts(search_query=""):
    listbox.delete(0, tk.END)
    if search_query:
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?", 
                       (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, f"ID:{row[0]} | {row[1]} | {row[2]} | {row[3]}")

def delete_contact():
    try:
        selected = listbox.get(listbox.curselection())
        contact_id = selected.split("|")[0].replace("ID:", "").strip()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Contact Deleted Successfully")
        view_contacts()
    except:
        messagebox.showerror("Error", "Please select a contact to delete")

def update_contact():
    try:
        selected = listbox.get(listbox.curselection())
        contact_id = selected.split("|")[0].replace("ID:", "").strip()
        
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        
        if name == "" or phone == "":
            messagebox.showwarning("Input Error", "Name and Phone are required!")
            return
        
        cursor.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", (name, phone, email, contact_id))
        conn.commit()
        messagebox.showinfo("Updated", "Contact Updated Successfully")
        clear_entries()
        view_contacts()
    except:
        messagebox.showerror("Error", "Please select a contact to update")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def search_contacts(event=None):
    search_query = entry_search.get()
    view_contacts(search_query)

def export_contacts():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        messagebox.showwarning("No Data", "No contacts to export!")
        return
    
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file:
        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Phone", "Email"])
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"Contacts exported successfully to {file}")

# GUI Setup
root = tk.Tk()
root.title("Smart Contact Book")
root.geometry("550x600")
root.config(bg="lightyellow")

# Title
tk.Label(root, text="Smart Contact Book", font=("Arial", 18, "bold"), bg="lightyellow").pack(pady=10)

# Search Bar
frame_search = tk.Frame(root, bg="lightyellow")
frame_search.pack(pady=5)
tk.Label(frame_search, text="Search:", bg="lightyellow").grid(row=0, column=0, padx=5)
entry_search = tk.Entry(frame_search, width=40)
entry_search.grid(row=0, column=1)
entry_search.bind("<KeyRelease>", search_contacts)

# Form
frame_form = tk.Frame(root, bg="lightyellow")
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name:", bg="lightyellow").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1)

tk.Label(frame_form, text="Phone:", bg="lightyellow").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_phone = tk.Entry(frame_form, width=30)
entry_phone.grid(row=1, column=1)

tk.Label(frame_form, text="Email:", bg="lightyellow").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_form, width=30)
entry_email.grid(row=2, column=1)

# Buttons
frame_buttons = tk.Frame(root, bg="lightyellow")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add", command=add_contact, bg="green", fg="white", width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update", command=update_contact, bg="blue", fg="white", width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete", command=delete_contact, bg="red", fg="white", width=12).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear", command=clear_entries, bg="orange", fg="white", width=12).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Export CSV", command=export_contacts, bg="purple", fg="white", width=12).grid(row=1, column=0, columnspan=4, pady=10)

# Listbox
listbox = tk.Listbox(root, width=75, height=15)
listbox.pack(pady=10)

# Load Contacts
view_contacts()

root.mainloop()

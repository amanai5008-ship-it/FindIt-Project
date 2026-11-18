import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Database connection
con = sqlite3.connect("findit.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    name TEXT,
    category TEXT,
    location TEXT,
    item_date TEXT,
    description TEXT
)
""")
con.commit()

# Main window
root = tk.Tk()
root.title("FindIt - Lost and Found Portal")
root.geometry("1000x650")
root.configure(bg="#f1f5f9")

BLUE = "#172554"
BG = "#f1f5f9"

# Sidebar
sidebar = tk.Frame(root, bg=BLUE, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="🔎 FindIt",
         font=("Arial", 25, "bold"),
         bg=BLUE, fg="white").pack(pady=35)

# Main area
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=30, pady=25)


# Clear main screen
def clear():
    for widget in main.winfo_children():
        widget.destroy()


# Dashboard
def dashboard():
    clear()

    tk.Label(main, text="Dashboard",
             font=("Arial", 28, "bold"),
             bg=BG, fg=BLUE).pack(anchor="w")

    tk.Label(main, text="Welcome to FindIt!",
             font=("Arial", 16),
             bg=BG, fg="#64748b").pack(anchor="w", pady=10)

    cur.execute("SELECT COUNT(*) FROM items WHERE type='Lost'")
    lost = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM items WHERE type='Found'")
    found = cur.fetchone()[0]

    cards = tk.Frame(main, bg=BG)
    cards.pack(fill="x", pady=30)

    for title, number, color in [
        ("Lost Items", lost, "#dc2626"),
        ("Found Items", found, "#16a34a"),
        ("Total Reports", lost + found, "#2563eb")
    ]:
        card = tk.Frame(cards, bg="white", padx=20, pady=30)
        card.pack(side="left", expand=True, fill="x", padx=8)

        tk.Label(card, text=number, font=("Arial", 28, "bold"),
                 fg=color, bg="white").pack()

        tk.Label(card, text=title, font=("Arial", 13, "bold"),
                 bg="white").pack()


# Report Lost form
def report_lost():
    clear()

    tk.Label(main, text="Report Lost Item",
             font=("Arial", 25, "bold"),
             bg=BG, fg=BLUE).pack(anchor="w", pady=15)

    fields = {}

    labels = [
        "Item Name",
        "Category",
        "Lost Location",
        "Date Lost (DD-MM-YYYY)",
        "Description"
    ]

    for label in labels:
        tk.Label(main, text=label, font=("Arial", 12, "bold"),
                 bg=BG).pack(anchor="w", pady=4)

        if label == "Description":
            entry = tk.Text(main, width=45, height=4,
                            font=("Arial", 11))
        else:
            entry = tk.Entry(main, width=45, font=("Arial", 11))

        entry.pack(anchor="w", pady=4)
        fields[label] = entry

    def submit():
        name = fields["Item Name"].get().strip()
        category = fields["Category"].get().strip()
        location = fields["Lost Location"].get().strip()
        item_date = fields["Date Lost (DD-MM-YYYY)"].get().strip()
        description = fields["Description"].get("1.0", "end").strip()

        if not all([name, category, location, item_date, description]):
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        cur.execute("""
        INSERT INTO items(type, name, category, location, item_date, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ("Lost", name, category, location, item_date, description))

        con.commit()

        messagebox.showinfo("Success", "Lost item reported successfully!")
        dashboard()

    tk.Button(main, text="Submit Report",
              command=submit,
              bg="#2563eb", fg="white",
              font=("Arial", 12, "bold"),
              padx=20, pady=10).pack(anchor="w", pady=15)

# Report Found form
def report_found():
    clear()

    tk.Label(main, text="Report Found Item",
             font=("Arial", 25, "bold"),
             bg=BG, fg=BLUE).pack(anchor="w", pady=15)

    fields = {}

    labels = [
        "Item Name",
        "Category",
        "Found Location",
        "Date Found (DD-MM-YYYY)",
        "Description"
    ]

    for label in labels:
        tk.Label(main, text=label,
                 font=("Arial", 12, "bold"),
                 bg=BG).pack(anchor="w", pady=4)

        if label == "Description":
            entry = tk.Text(main, width=45, height=4,
                            font=("Arial", 11))
        else:
            entry = tk.Entry(main, width=45,
                             font=("Arial", 11))

        entry.pack(anchor="w", pady=4)
        fields[label] = entry

    def submit():
        name = fields["Item Name"].get().strip()
        category = fields["Category"].get().strip()
        location = fields["Found Location"].get().strip()
        item_date = fields["Date Found (DD-MM-YYYY)"].get().strip()
        description = fields["Description"].get("1.0", "end").strip()

        if not all([name, category, location, item_date, description]):
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        cur.execute("""
        INSERT INTO items(type, name, category, location, item_date, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ("Found", name, category, location, item_date, description))

        con.commit()

        messagebox.showinfo("Success", "Found item reported successfully!")
        dashboard()

    tk.Button(main, text="Submit Report",
              command=submit,
              bg="#16a34a", fg="white",
              font=("Arial", 12, "bold"),
              padx=20, pady=10).pack(anchor="w", pady=15)
# Search Items
def search_items():
    clear()

    tk.Label(main, text="Search Items",
             font=("Arial", 25, "bold"),
             bg=BG, fg=BLUE).pack(anchor="w", pady=15)

    tk.Label(main, text="Enter item name, category or location:",
             font=("Arial", 12), bg=BG).pack(anchor="w")

    search_box = tk.Entry(main, width=40, font=("Arial", 12))
    search_box.pack(anchor="w", pady=10)

    results = tk.Listbox(main, width=85, height=18,
                         font=("Arial", 11))
    results.pack(pady=15, fill="both", expand=True)

    def search():
        results.delete(0, tk.END)

        word = search_box.get().strip()

        cur.execute("""
        SELECT id, type, name, category, location, item_date
        FROM items
        WHERE name LIKE ? OR category LIKE ? OR location LIKE ?
        """, ('%' + word + '%', '%' + word + '%', '%' + word + '%'))

        rows = cur.fetchall()

        if not rows:
            results.insert(tk.END, "No matching items found.")
            return

        for row in rows:
            results.insert(
                tk.END,
                f"ID: {row[0]} | {row[1]} | {row[2]} | "
                f"{row[3]} | {row[4]} | {row[5]}"
            )

    tk.Button(main, text="Search",
              command=search,
              bg="#2563eb", fg="white",
              font=("Arial", 12, "bold"),
              padx=20, pady=8).pack(anchor="w")

    search()
def view_records():
    clear()

    tk.Label(main, text="All Records",
             font=("Arial", 22, "bold"),
             bg=BG, fg=BLUE).pack(pady=20)

    table = ttk.Treeview(
        main,
        columns=("ID", "Type", "Name", "Category", "Location", "Date"),
        show="headings"
    )

    for col in ("ID", "Type", "Name", "Category", "Location", "Date"):
        table.heading(col, text=col)
        table.column(col, width=130)

    table.pack(fill="both", expand=True, padx=20, pady=20)

    cur.execute("""
        SELECT id, type, name, category, location, item_date
        FROM items
    """)

    for record in cur.fetchall():
        table.insert("", "end", values=record)
def delete_record():
    clear()

    tk.Label(main, text="Delete Record",
             font=("Arial", 22, "bold"),
             bg=BG, fg=BLUE).pack(pady=20)

    table = ttk.Treeview(
        main,
        columns=("ID", "Type", "Name", "Category", "Location", "Date"),
        show="headings"
    )

    for col in ("ID", "Type", "Name", "Category", "Location", "Date"):
        table.heading(col, text=col)
        table.column(col, width=130)

    table.pack(fill="both", expand=True, padx=20, pady=20)

    def load_records():
        for row in table.get_children():
            table.delete(row)

        cur.execute("""
            SELECT id, type, name, category, location, item_date
            FROM items
        """)

        for record in cur.fetchall():
            table.insert("", "end", values=record)

    def delete_selected():
        selected = table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a record!")
            return

        record_id = table.item(selected[0], "values")[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?"
        )

        if confirm:
            cur.execute("DELETE FROM items WHERE id = ?", (record_id,))
            con.commit()
            messagebox.showinfo("Success", "Record deleted!")
            load_records()

    load_records()

    tk.Button(main, text="Delete Selected Record",
              command=delete_selected,
              bg="red", fg="white",
              font=("Arial", 12, "bold")).pack(pady=10)
# Other buttons (we will develop these next)
def coming_soon(name):
    messagebox.showinfo("FindIt", name + " feature coming soon!")


# Sidebar buttons
buttons = [
    ("🏠 Dashboard", dashboard),
    ("📢 Report Lost", report_lost),
    ("📦 Report Found", report_found),
    ("🔍 Search Items", search_items),
    ("📋 View Records", view_records),
    ("🗑️ Delete Record", delete_record),
]

for name, command in buttons:
    tk.Button(sidebar, text=name, command=command,
              font=("Arial", 12), bg=BLUE, fg="white",
              activebackground="#1e40af",
              relief="flat", pady=14).pack(fill="x", padx=8)

tk.Button(sidebar, text="Exit", command=root.destroy,
          bg="#dc2626", fg="white",
          font=("Arial", 12, "bold"),
          relief="flat", pady=12).pack(side="bottom",
                                       fill="x", padx=10, pady=20)

dashboard()
root.mainloop()
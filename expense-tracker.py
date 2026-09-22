import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


# =========================
# Data
# =========================

expenses = []

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")

categories = [
    "Life Expenses",
    "Electricity",
    "Gas",
    "Rental",
    "Grocery",
    "Savings",
    "Education",
    "Charity"
]


# =========================
# Colors
# =========================

BG = "#0f172a"
CARD = "#1e293b"
INPUT = "#334155"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
BLUE = "#38bdf8"
RED = "#ef4444"


# =========================
# Functions
# =========================

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f)


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for expense in data:
                if not isinstance(expense, dict):
                    expense = {
                        "amount": expense[0],
                        "currency": expense[1],
                        "category": expense[2],
                        "date": expense[3],
                        "payment": expense[4]
                    }
                expenses.append(expense)
                table.insert(
                    "",
                    "end",
                    values=(
                        f"{expense['amount']:.2f}",
                        expense["currency"],
                        expense["category"],
                        expense["date"],
                        expense["payment"]
                    )
                )
        save_expenses()
        update_totals()


def add_expense():

    amount = amount_entry.get().strip()
    currency = currency_combo.get()
    category = category_combo.get().strip()
    date = date_entry.get().strip()
    payment = payment_combo.get()

    # Check empty fields
    if not amount or not category or not date:
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    # Check amount
    try:
        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid positive amount."
        )
        return

    # Check date
    try:
        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Date must be in YYYY-MM-DD format."
        )
        return

    # Add new category to the list
    if category not in categories:

        categories.append(category)

        category_combo["values"] = categories

    # Create expense
    expense = {
        "amount": amount,
        "currency": currency,
        "category": category,
        "date": date,
        "payment": payment
    }

    expenses.append(expense)

    save_expenses()

    # Add expense to table
    table.insert(
        "",
        "end",
        values=(
            f"{amount:.2f}",
            currency,
            category,
            date,
            payment
        )
    )

    update_totals()
    clear_form()


def update_totals():

    usd = 0
    eur = 0
    egp = 0

    for expense in expenses:

        if expense["currency"] == "USD":
            usd += expense["amount"]

        elif expense["currency"] == "EUR":
            eur += expense["amount"]

        elif expense["currency"] == "EGP":
            egp += expense["amount"]

    usd_label.config(
        text=f"${usd:.2f}"
    )

    eur_label.config(
        text=f"€{eur:.2f}"
    )

    egp_label.config(
        text=f"£{egp:.2f}"
    )


def delete_expense():

    selected = table.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select an expense first."
        )

        return

    confirm = messagebox.askyesno(
        "Delete Expense",
        "Are you sure you want to delete this expense?"
    )

    if not confirm:
        return

    item = selected[0]

    index = table.index(item)

    table.delete(item)

    expenses.pop(index)

    save_expenses()

    update_totals()


def clear_form():

    amount_entry.delete(
        0,
        tk.END
    )

    currency_combo.set(
        "USD"
    )

    category_combo.set(
        ""
    )

    payment_combo.set(
        "Cash"
    )

    date_entry.delete(
        0,
        tk.END
    )

    date_entry.insert(
        0,
        datetime.now().strftime(
            "%Y-%m-%d"
        )
    )


# =========================
# Main Window
# =========================

window = tk.Tk()

window.title(
    "Expense Tracker"
)

window.geometry(
    "1050x700"
)

window.minsize(
    900,
    600
)

window.configure(
    bg=BG
)


# =========================
# Style
# =========================

style = ttk.Style()

style.theme_use(
    "clam"
)

style.configure(
    "Treeview",
    background=CARD,
    foreground=TEXT,
    fieldbackground=CARD,
    rowheight=38,
    borderwidth=0,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=INPUT,
    foreground=TEXT,
    font=("Arial", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[
        ("selected", "#075985")
    ]
)


# =========================
# Header
# =========================

header = tk.Frame(
    window,
    bg=BG
)

header.pack(
    fill="x",
    padx=30,
    pady=(25, 10)
)


tk.Label(
    header,
    text="Expense Tracker",
    bg=BG,
    fg=TEXT,
    font=("Arial", 28, "bold")
).pack(
    anchor="w"
)


tk.Label(
    header,
    text="Track and manage your daily expenses",
    bg=BG,
    fg=MUTED,
    font=("Arial", 11)
).pack(
    anchor="w"
)


# =========================
# Summary Cards
# =========================

summary = tk.Frame(
    window,
    bg=BG
)

summary.pack(
    fill="x",
    padx=30,
    pady=15
)


def create_card(
    parent,
    title,
    value,
    column
):

    card = tk.Frame(
        parent,
        bg=CARD
    )

    card.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=6
    )

    parent.columnconfigure(
        column,
        weight=1
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 0)
    )

    label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=TEXT,
        font=("Arial", 22, "bold")
    )

    label.pack(
        anchor="w",
        padx=18,
        pady=(3, 15)
    )

    return label


usd_label = create_card(
    summary,
    "USD",
    "$0.00",
    0
)

eur_label = create_card(
    summary,
    "EUR",
    "€0.00",
    1
)

egp_label = create_card(
    summary,
    "EGP",
    "£0.00",
    2
)


# =========================
# Add Expense Section
# =========================

form = tk.Frame(
    window,
    bg=CARD
)

form.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Label(
    form,
    text="Add New Expense",
    bg=CARD,
    fg=TEXT,
    font=("Arial", 16, "bold")
).grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="w",
    padx=20,
    pady=(18, 12)
)


# =========================
# Amount
# =========================

tk.Label(
    form,
    text="Amount",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10, "bold")
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=20
)


amount_entry = tk.Entry(
    form,
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    font=("Arial", 10)
)

amount_entry.grid(
    row=2,
    column=0,
    padx=20,
    pady=(5, 15),
    ipady=7
)


# =========================
# Currency
# =========================

tk.Label(
    form,
    text="Currency",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10, "bold")
).grid(
    row=1,
    column=1,
    sticky="w",
    padx=10
)


currency_combo = ttk.Combobox(
    form,
    values=[
        "USD",
        "EUR",
        "EGP"
    ],
    state="readonly"
)

currency_combo.grid(
    row=2,
    column=1,
    padx=10,
    pady=(5, 15)
)

currency_combo.set(
    "USD"
)


# =========================
# Expense For
# =========================

tk.Label(
    form,
    text="Expense For",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10, "bold")
).grid(
    row=1,
    column=2,
    sticky="w",
    padx=10
)


category_combo = ttk.Combobox(
    form,
    values=categories
)

category_combo.grid(
    row=2,
    column=2,
    padx=10,
    pady=(5, 15)
)


# =========================
# Date
# =========================

tk.Label(
    form,
    text="Date",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10, "bold")
).grid(
    row=3,
    column=0,
    sticky="w",
    padx=20
)


date_entry = tk.Entry(
    form,
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    font=("Arial", 10)
)

date_entry.grid(
    row=4,
    column=0,
    padx=20,
    pady=(5, 18),
    ipady=7
)

date_entry.insert(
    0,
    datetime.now().strftime(
        "%Y-%m-%d"
    )
)


# =========================
# Payment
# =========================

tk.Label(
    form,
    text="Payment Method",
    bg=CARD,
    fg=MUTED,
    font=("Arial", 10, "bold")
).grid(
    row=3,
    column=1,
    sticky="w",
    padx=10
)


payment_combo = ttk.Combobox(
    form,
    values=[
        "Cash",
        "Credit Card",
        "Paypal"
    ],
    state="readonly"
)

payment_combo.grid(
    row=4,
    column=1,
    padx=10,
    pady=(5, 18)
)

payment_combo.set(
    "Cash"
)


# =========================
# Add Button
# =========================

add_button = tk.Button(
    form,
    text="+  Add Expense",
    command=add_expense,
    bg=BLUE,
    fg="#082f49",
    activebackground="#7dd3fc",
    activeforeground="#082f49",
    font=("Arial", 11, "bold"),
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=9
)

add_button.grid(
    row=4,
    column=2,
    padx=10,
    pady=(5, 18)
)


# =========================
# Expense History
# =========================

history = tk.Frame(
    window,
    bg=BG
)

history.pack(
    fill="x",
    padx=30,
    pady=(20, 5)
)


tk.Label(
    history,
    text="Expense History",
    bg=BG,
    fg=TEXT,
    font=("Arial", 17, "bold")
).pack(
    side="left"
)


delete_button = tk.Button(
    history,
    text="Delete Selected",
    command=delete_expense,
    bg=RED,
    fg="white",
    activebackground="#dc2626",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=7
)

delete_button.pack(
    side="right"
)


# =========================
# Table
# =========================

table_frame = tk.Frame(
    window,
    bg=CARD
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(5, 25)
)


columns = (
    "Amount",
    "Currency",
    "Expense For",
    "Date",
    "Payment"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        anchor="center",
        width=170
    )


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(
    yscrollcommand=scrollbar.set
)


table.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0),
    pady=10
)


scrollbar.pack(
    side="right",
    fill="y",
    padx=(0, 10),
    pady=10
)


# =========================
# Start Application
# =========================

load_expenses()

window.mainloop()
# ExpenseTracker

A simple desktop expense tracker that helps you log and manage your daily spending across multiple currencies.

## Features

- 📊 Track expenses in multiple currencies (USD, EUR, EGP)
- 💳 Payment method tracking (Cash, Credit Card, Paypal)
- 🏷️ Categories with the ability to add your own on the fly
- 📅 Date-based expense logging
- 📋 Expense history table with a scrollable view
- 🗑️ Delete a selected expense
- 💰 Live per-currency balance summary cards (USD / EUR / EGP)
- 📱 Clean dark-theme UI built with Tkinter
- 💾 All data stored locally on your device — no internet or account required

## Tech Stack

- **Language:** Python 3
- **Framework:** Tkinter (Python standard library)
- **Storage:** Local JSON file (`expenses.json`) — no external database or server

## Getting Started

### Prerequisites

- Python 3.7+ installed on your machine
- Tkinter (included with Python on Windows; on Linux install via your package manager, e.g. `sudo apt install python3-tk`)

### Installation

```bash
# Clone the repository
git clone https://github.com/ebrahemsaeed911-lang/ExpenseTracker

# Navigate into the project folder
cd ExpenseTracker

# No extra packages required — Tkinter ships with Python

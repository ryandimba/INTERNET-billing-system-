import sqlite3
from datetime import datetime, timedelta

# ---------------- Database Setup ----------------
conn = sqlite3.connect("billing.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    speed TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    plan_id INTEGER,
    amount REAL,
    due_date TEXT,
    status TEXT DEFAULT 'Unpaid',
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(plan_id) REFERENCES plans(id)
)
""")
conn.commit()


# ---------------- Functions ----------------
def add_customer(name, email):
    cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    print("✅ Customer added successfully.")


def add_plan(name, speed, price):
    cursor.execute("INSERT INTO plans (name, speed, price) VALUES (?, ?, ?)", (name, speed, price))
    conn.commit()
    print("✅ Plan added successfully.")


def generate_bill(customer_id, plan_id, days=30):
    cursor.execute("SELECT price FROM plans WHERE id=?", (plan_id,))
    plan = cursor.fetchone()
    if not plan:
        print("❌ Plan not found.")
        return
    price = plan[0]
    due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO bills (customer_id, plan_id, amount, due_date) VALUES (?, ?, ?, ?)",
        (customer_id, plan_id, price, due_date)
    )
    conn.commit()
    print("✅ Bill generated successfully.")


def view_bills():
    cursor.execute("""
    SELECT b.id, c.name, p.name, b.amount, b.due_date, b.status
    FROM bills b
    JOIN customers c ON b.customer_id = c.id
    JOIN plans p ON b.plan_id = p.id
    """)
    rows = cursor.fetchall()
    print("\n📋 Bills:")
    if not rows:
        print("No bills found.")
    for row in rows:
        print(f"BillID: {row[0]} | Customer: {row[1]} | Plan: {row[2]} | Amount: {row[3]} | Due: {row[4]} | Status: {row[5]}")


def pay_bill(bill_id):
    cursor.execute("UPDATE bills SET status='Paid' WHERE id=?", (bill_id,))
    conn.commit()
    print("✅ Bill paid successfully.")


# ---------------- Main Program ----------------
print("📡 Internet Billing System")

while True:

        print("\n1. Add Customer\n2. Add Plan\n3. Generate Bill\n4. View Bills\n5. Pay Bill\n6. Exit")
        choice = input("Enter choice: ").strip()   # <--- strip() to avoid hidden chars

        if choice == "1":
            name = input("Customer Name: ")
            email = input("Customer Email: ")
            add_customer(name, email)

        elif choice == "2":
            name = input("Plan Name: ")
            speed = input("Speed (e.g., 10Mbps): ")
            price = float(input("Price: "))
            add_plan(name, speed, price)

        elif choice == "3":
            customer_id = int(input("Customer ID: "))
            plan_id = int(input("Plan ID: "))
            generate_bill(customer_id, plan_id)

        elif choice == "4":
            view_bills()

        elif choice == "5":
            bill_id = int(input("Bill ID to pay: "))
            pay_bill(bill_id)

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice, try again.")
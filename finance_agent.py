from datetime import datetime
import uuid
import os
import json
import ollama

FILE_NAME = "transactions.json"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as file:
        json.dump([], file)


def load_transactions():
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_transactions(transactions):
    with open(FILE_NAME, "w") as file:
        json.dump(transactions, file, indent=4)


def add_transaction(transaction_type, amount, description):
    transactions = load_transactions()

    transactions.append({
        "id": str(uuid.uuid4()),
        "type": transaction_type.lower(),
        "amount": float(amount),
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_transactions(transactions)


def delete_transaction(transaction_id):
    transactions = load_transactions()

    transactions = [
        t for t in transactions
        if t["id"] != transaction_id
    ]

    save_transactions(transactions)


def get_summary():
    transactions = load_transactions()

    income = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "income"
    )

    expense = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "expense"
    )

    return {
        "income": income,
        "expense": expense,
        "savings": income - expense
    }


def get_transactions():
    transactions = load_transactions()

    incomes = [
        t for t in transactions
        if t["type"] == "income"
    ]

    expenses = [
        t for t in transactions
        if t["type"] == "expense"
    ]

    return incomes, expenses


def ask_ai(question):
    transactions = load_transactions()

    prompt = f"""
You are an AI financial assistant.

User Transactions:
{transactions}

Financial Summary:
{get_summary()}

Answer the user's question using the above data.

Question:
{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
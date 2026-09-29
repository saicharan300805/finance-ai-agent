from flask import Flask, render_template, request, redirect, url_for, session
from finance_agent import delete_transaction
from finance_agent import (
    add_transaction,
    get_summary,
    get_transactions,
    ask_ai
)

app = Flask(__name__)
app.secret_key = "finance_secret_key"


@app.route("/")
def home():
    summary = get_summary()
    incomes, expenses = get_transactions()

    answer = session.pop("answer", None)

    return render_template(
        "index.html",
        summary=summary,
        incomes=incomes,
        expenses=expenses,
        answer=answer
    )
@app.route("/delete/<transaction_id>")
def delete(transaction_id):
    delete_transaction(transaction_id)
    return redirect(url_for("home"))

@app.route("/add", methods=["POST"])
def add():
    transaction_type = request.form["type"]
    amount = float(request.form["amount"])
    description = request.form["description"]

    add_transaction(
        transaction_type,
        amount,
        description
    )

    return redirect(url_for("home"))


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    answer = ask_ai(question)

    # Store answer temporarily
    session["answer"] = answer

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
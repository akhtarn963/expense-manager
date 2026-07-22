def format_money(amount):
    return f"Rs. {amount:,}"

def calculate_statistics(expenses):
    total_expense = sum(expense.amount for expense in expenses)
    total_records = len(expenses)
    highest_expense = max((expense.amount for expense in expenses), default=0)
    lowest_expense = min((expense.amount for expense in expenses), default=0)
    average_expense = total_expense / total_records if total_records > 0 else 0
    return {
        "total_expense": total_expense,
        "total_records": total_records,
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense,
        "average_expense": average_expense
    }
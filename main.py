class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            description = entry["description"][:23].ljust(23)
            amount = f"{entry['amount']:.2f}".rjust(7)
            items += f"{description}{amount}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    spent_amounts = []
    for category in categories:
        total_spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        spent_amounts.append(total_spent)

    total_spent = sum(spent_amounts)
    spent_percentages = [(amount / total_spent) * 100 if total_spent > 0 else 0 for amount in spent_amounts]

    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percent in spent_percentages:
            chart += "o  " if percent >= i else "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_length = max(len(category.name) for category in categories)
    names = [category.name.ljust(max_length) for category in categories]

    for x in zip(*names):
        chart += "     " + "  ".join(x) + "  \n"

    return chart.rstrip() + "  "

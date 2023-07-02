import pandas as pd
from scipy import optimize


def get_yearly_payment(loan: float, interest_rate: float, tenor=30) -> float:
    def func(payment):
        balance = loan
        for i in range(tenor):
            interest = balance * interest_rate / 100.0
            balance = balance + interest - payment
            # print(payment, balance)
        return balance

    return round(optimize.fsolve(func, [loan / 20])[0], 2)


def loan_burn_down_df(
    buy_price: float, loan: float, payment: float, interest_rate: float, house_rate: float, tenor=30
) -> pd.DataFrame:
    rows = []
    balance = loan
    price = buy_price
    for i in range(1, tenor + 1):
        new_price = round(price * (1 + house_rate / 100.0), 2)
        interest = round(balance * interest_rate / 100.0, 2)
        new_balance = balance + interest - payment
        d = {
            "Year": i,
            "Starting house value": price,
            "Ending house value": new_price,
            "Starting Loan balance": balance,
            "Interest": interest,
            "Principal": payment - interest,
            "Ending Loan balance": new_balance,
            "End of year equity": new_price - new_balance,
        }
        balance = new_balance
        price = new_price
        rows.append(d)

    return pd.DataFrame.from_records(rows).set_index("Year")


def stock_df(starting_balance: float, stock_rate: float, contributions: float, tenor=30) -> pd.DataFrame:
    rows = []
    balance = starting_balance
    for i in range(1, tenor + 1):
        gains = balance * stock_rate / 100.0
        new_balance = round(balance + gains + contributions, 2)
        d = {
            "Year": i,
            "Starting balance": balance,
            "Gains": gains,
            "Contributions": contributions,
            "Ending balance": new_balance,
        }
        balance = new_balance
        rows.append(d)

    return pd.DataFrame.from_records(rows).set_index("Year")

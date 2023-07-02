import streamlit as st

from loan import get_yearly_payment, loan_burn_down_df, stock_df

st.set_page_config(page_title="House prices", layout="wide")
st.title("House prices")

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    buy_price = st.number_input("House buy price", value=1_000_000, step=10_000, format="%d")
    deposit = st.number_input("Deposit", value=200_000, step=5000, format="%d")
    stamp_duty = 0.05 * buy_price
    st.text_input("Stamp duty", value=stamp_duty, disabled=True)
    loan = buy_price - deposit
    st.text_input("Loan", value=loan, disabled=True)
    tenor = st.number_input(
        "Investment timeframe (years)", value=30, step=1, min_value=10, max_value=100, format="%d"
    )
with col2:
    tax_rate = st.number_input("Tax rate (%)", value=35, min_value=0, step=1, format="%d")
    interest_rate = st.number_input("Interest rate (%)", value=8.0, min_value=0.0, step=0.5, format="%f")
    housing_rate = st.number_input("House price CAGR (%)", value=8.0, min_value=0.0, step=0.5, format="%f")
    stock_Rate = st.number_input("Share market CAGR (%)", value=10.0, min_value=0.0, step=0.5, format="%f")
    payment = get_yearly_payment(loan, interest_rate)
    st.text_input("Mortgage payment (yearly)", value=payment, disabled=True)
with col3:
    rent = st.number_input("Rent (per week)", value=600, step=10, format="%d") * 52
    agent_fees = st.number_input("Agent fees (%)", value=5.0, step=0.5, format="%f")
    costs = st.number_input("Other costs", value=5000, step=100, format="%d")
    income = rent * (100 - agent_fees) / 100 - costs
    st.text_input("Net rental income", value=income, disabled=True)
    st.text_input("Net mortgage payment", value=round(payment - income, 2), disabled=True)
    net_payment = round((payment - income) * (1 - tax_rate / 100), 2)
    st.text_input("Net mortgage payment after tax", value=net_payment, disabled=True)


house_returns = loan_burn_down_df(buy_price, loan, payment, interest_rate, housing_rate, tenor)
df_height = height = int(35.19 * (len(house_returns) + 1))
col1, col2 = st.columns([0.6, 0.4], gap="large")
with col1:
    st.subheader(f"House and loan over {tenor} years")
    st.dataframe(house_returns, use_container_width=True, height=df_height)

stock_returns = stock_df(deposit + stamp_duty, stock_Rate, net_payment, tenor)
with col2:
    st.subheader(f"Stock market over {tenor} years")
    st.dataframe(stock_returns, use_container_width=True, height=df_height)

_, col2, _ = st.columns([0.25, 0.5, 0.25], gap="large")
with col2:
    df = house_returns[["End of year equity"]].join(stock_returns[["Ending balance"]])
    df.rename(columns={"End of year equity": "House", "Ending balance": "Shares"}, inplace=True)
    st.line_chart(df, use_container_width=True, height=800)

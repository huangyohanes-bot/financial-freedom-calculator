import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Financial Freedom Calculator",
    layout="centered"
)

st.title("💰 Financial Freedom Calculator")
st.write("Simulate when your savings can generate enough income to cover your monthly expenses.")

# =========================
# INPUT SECTION
# =========================

st.header("📥 Monthly Financial Data")

current_savings = st.number_input("Current Savings (Rp)", value=100_000_000)
monthly_income = st.number_input("Monthly Income (Rp)", value=10_000_000)
monthly_expenses = st.number_input("Monthly Expenses (Rp)", value=6_000_000)

monthly_savings = monthly_income - monthly_expenses

# =========================
# DEPOSIT SETTINGS
# =========================

st.header("🏦 Deposit Settings")

deposit_rate = st.slider("Annual Deposit Rate (%)", 0.0, 10.0, 5.0) / 100

tenor_months = st.selectbox(
    "Deposit Duration",
    [1, 3, 6, 12],
    format_func=lambda x: f"{x} month(s)"
)

# =========================
# SIMULATION FUNCTION
# =========================

def simulate_months(
    savings,
    monthly_savings,
    monthly_expenses,
    deposit_rate,
    tenor_months,
    max_months=1200
):
    S = savings
    data = []

    period_rate = deposit_rate * (tenor_months / 12)

    for month in range(1, max_months + 1):

        # Apply deposit interest at end of tenor
        if month % tenor_months == 0:
            S = S * (1 + period_rate)

        # Monthly passive income estimation
        monthly_yield = deposit_rate / 12
        investment_income = S * monthly_yield

        data.append({
            "Month": month,
            "Net Worth": S,
            "Investment Income": investment_income
        })

        # Check financial freedom condition
        if investment_income >= monthly_expenses:
            return month, pd.DataFrame(data)

        # Add monthly savings
        S += monthly_savings

    return None, pd.DataFrame(data)

# =========================
# RUN SIMULATION
# =========================

months, df = simulate_months(
    current_savings,
    monthly_savings,
    monthly_expenses,
    deposit_rate,
    tenor_months
)

# =========================
# RESULTS
# =========================

st.header("📊 Results")

monthly_yield = deposit_rate / 12 if deposit_rate > 0 else 0
required_wealth = monthly_expenses / monthly_yield if monthly_yield > 0 else 0

st.metric("Required Wealth (Rp)", f"{required_wealth:,.0f}")
st.metric("Monthly Savings (Rp)", f"{monthly_savings:,.0f}")

if months is not None:
    years = months // 12
    remaining_months = months % 12
    st.success(f"🎯 Financial freedom in **{years} years {remaining_months} months**")
else:
    st.warning("⚠️ Not reached within simulation period")

# =========================
# CHARTS
# =========================

st.subheader("📈 Net Worth Growth")
st.line_chart(df.set_index("Month")["Net Worth"])

st.subheader("💸 Investment Income Growth")
st.line_chart(df.set_index("Month")["Investment Income"])

# =========================
# SCENARIO COMPARISON
# =========================

st.header("🔍 Scenario Comparison")

increase_savings_pct = st.slider("Increase Savings (%)", 0, 100, 20)

new_monthly_savings = monthly_savings * (1 + increase_savings_pct / 100)

months_new, _ = simulate_months(
    current_savings,
    new_monthly_savings,
    monthly_expenses,
    deposit_rate,
    tenor_months
)

col1, col2 = st.columns(2)

with col1:
    if months:
        st.metric("Current Plan", f"{months//12}y {months%12}m")
    else:
        st.metric("Current Plan", "Not reached")

with col2:
    if months_new:
        st.metric("Improved Savings", f"{months_new//12}y {months_new%12}m")
    else:
        st.metric("Improved Savings", "Not reached")

# =========================
# INSIGHT SECTION
# =========================

st.header("🧠 Insight")

if months and months_new:
    diff = months - months_new
    st.write(f"Increasing savings helps you reach freedom **{diff//12} years {diff%12} months faster**.")

st.write("Financial freedom = investment income ≥ monthly expenses.")

# =========================
# FOOTNOTE
# =========================

st.caption("Note: This simulation assumes constant income, expenses, and deposit rate. Real outcomes may vary.")
import streamlit as st

def generate_insights(df):
    st.header("🧠 Smart Insights")

    income = df[df["type"]=="Income"]["amount"].sum()
    expense = df[df["type"]=="Expense"]["amount"].sum()

    if income == 0:
        st.warning("No income recorded.")
        return

    savings = income - expense

    if savings >= 0:
        st.success(f"✅ You saved ₹{savings:.2f} this period.")
    else:
        st.error("🚨 You are spending more than your income!")

    exp_df = df[df["type"]=="Expense"]

    if not exp_df.empty:
        totals = exp_df.groupby("category")["amount"].sum()
        top_cat = totals.idxmax()
        percent = (totals.max() / expense) * 100

        st.info(f"📌 Top expense category: **{top_cat}** ({percent:.1f}%)")

        if percent > 30:
            st.warning(f"⚠️ Overspending on **{top_cat}**")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_charts(df):
    df["date"] = pd.to_datetime(df["date"])

    income = df[df["type"]=="Income"]["amount"].sum()
    expense = df[df["type"]=="Expense"]["amount"].sum()

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots()
        ax.bar(["Income","Expense"], [income, expense])
        ax.set_title("Income vs Expense")
        st.pyplot(fig)

    with c2:
        exp_df = df[df["type"]=="Expense"]
        if not exp_df.empty:
            fig2, ax2 = plt.subplots()
            exp_df.groupby("category")["amount"].sum().plot.pie(
                autopct="%1.1f%%", ax=ax2
            )
            ax2.set_title("Category-wise Expense")
            ax2.set_ylabel("")
            st.pyplot(fig2)

    st.subheader("📈 Monthly Spending Trend")

    monthly = (
        df[df["type"]=="Expense"]
        .groupby(df["date"].dt.to_period("M"))["amount"]
        .sum()
    )

    fig3, ax3 = plt.subplots()
    monthly.plot(marker="o", ax=ax3)
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Amount")
    st.pyplot(fig3)

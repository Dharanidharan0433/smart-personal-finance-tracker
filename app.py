import streamlit as st
import pandas as pd
from datetime import date
from charts import show_charts
from insights import generate_insights

st.set_page_config(page_title="Smart Finance Tracker", layout="wide")
st.title("💸 Smart Personal Finance Tracker")

DATA_FILE = "data.csv"

# ---------- Load Data ----------
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["date","amount","type","category","description"])

df = load_data()

# ---------- ADD TRANSACTION ----------
st.header("➕ Add Transaction")

with st.form("add_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        t_date = st.date_input("Date", date.today())
    with c2:
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
    with c3:
        t_type = st.selectbox("Type", ["Income", "Expense"])

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
    )
    description = st.text_input("Description")

    submit = st.form_submit_button("Add")

    if submit:
        new_row = {
            "date": t_date,
            "amount": amount,
            "type": t_type,
            "category": category,
            "description": description
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Transaction added!")
        st.rerun()

# ---------- VIEW DATA ----------
st.header("📄 View Transactions")
st.dataframe(df.reset_index())

# ---------- DELETE ----------
st.header("🗑️ Delete Transaction")

if not df.empty:
    del_index = st.number_input(
        "Enter index to delete",
        min_value=0,
        max_value=len(df)-1,
        step=1
    )

    if st.button("Delete"):
        df = df.drop(index=del_index)
        df.to_csv(DATA_FILE, index=False)
        st.success("Deleted successfully!")
        st.rerun()

# ---------- EDIT ----------
st.header("✏️ Edit Transaction")

if not df.empty:
    edit_index = st.number_input(
        "Enter index to edit",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="edit"
    )

    row = df.loc[edit_index]

    new_date = st.date_input("Edit Date", pd.to_datetime(row["date"]))
    new_amount = st.number_input("Edit Amount", value=float(row["amount"]))
    new_type = st.selectbox(
        "Edit Type", ["Income","Expense"],
        index=0 if row["type"]=="Income" else 1
    )
    new_category = st.selectbox(
        "Edit Category",
        ["Food","Travel","Shopping","Bills","Entertainment","Other"],
        index=["Food","Travel","Shopping","Bills","Entertainment","Other"].index(row["category"])
    )
    new_desc = st.text_input("Edit Description", row["description"])

    if st.button("Update"):
        df.loc[edit_index, "date"] = new_date
        df.loc[edit_index, "amount"] = new_amount
        df.loc[edit_index, "type"] = new_type
        df.loc[edit_index, "category"] = new_category
        df.loc[edit_index, "description"] = new_desc

        df.to_csv(DATA_FILE, index=False)
        st.success("Updated successfully!")
        st.rerun()


# ---------- DASHBOARD ----------
st.header("📊 Dashboard")

if df.empty:
    st.info("No data available.")
else:
    show_charts(df)
    generate_insights(df)

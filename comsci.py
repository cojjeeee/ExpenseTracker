import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="XTrack - Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #AFC3A5;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: #212F19;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #405535;
    }

    .metric-title {
        font-size: 15px;
        color: #B7C9AE;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #E5F0DE;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .analysis-box {
        background-color: #314524;
        padding: 18px;
        border-radius: 12px;
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

data = pd.read_csv("personalexpense.csv")

# Convert Date into datetime
data["Date"] = pd.to_datetime(data["Date"], format="mixed")

# Make sure Price is numeric
data["Price"] = pd.to_numeric(data["Price"], errors="coerce")

# Remove invalid rows if there are any
data = data.dropna(subset=["Price", "Date"])

# Clean category names
data["Category"] = data["Category"].replace({
    "Foods": "Food"
})


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💰 XTrack")

st.sidebar.write("Student Expense Tracker")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🧾 Expenses",
        "📊 Analytics",
        "💰 Budget"
    ]
)

st.sidebar.divider()

# Budget input
budget = st.sidebar.number_input(
    "Monthly Budget",
    min_value=0.0,
    value=5000.0,
    step=100.0
)


# =========================================================
# BASIC CALCULATIONS
# =========================================================

# NumPy is used for numerical calculations
total_expense = np.sum(data["Price"])

average_expense = np.mean(data["Price"])

highest_expense = np.max(data["Price"])

lowest_expense = np.min(data["Price"])

number_of_expenses = len(data)

# Current month
current_month = data["Date"].max().to_period("M")

monthly_data = data[
    data["Date"].dt.to_period("M") == current_month
]

monthly_total = np.sum(monthly_data["Price"])

# Remaining budget
remaining_budget = budget - monthly_total

# Budget percentage
if budget > 0:
    budget_percentage = (monthly_total / budget) * 100
else:
    budget_percentage = 0


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<p class="main-title">💰 XTrack</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">'
        'Student Personal Expense and Budget Tracker'
        '</p>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SUMMARY CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Expenses</div>
                <div class="metric-value">₱{total_expense:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Average Expense</div>
                <div class="metric-value">₱{average_expense:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Highest Expense</div>
                <div class="metric-value">₱{highest_expense:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        if remaining_budget >= 0:
            budget_text = f"₱{remaining_budget:,.2f}"
        else:
            budget_text = f"-₱{abs(remaining_budget):,.2f}"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Remaining Budget</div>
                <div class="metric-value">{budget_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # -----------------------------------------------------
    # BUDGET PROGRESS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">💳 Monthly Budget</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Monthly spending: **₱{monthly_total:,.2f} / ₱{budget:,.2f}**"
    )

    progress = min(max(budget_percentage / 100, 0), 1)

    st.progress(progress)

    st.write(
        f"Budget used: **{budget_percentage:.2f}%**"
    )

    if budget_percentage >= 100:
        st.error("⚠️ You have exceeded your monthly budget.")

    elif budget_percentage >= 80:
        st.warning("⚠️ You are approaching your monthly budget.")

    else:
        st.success("✅ Your spending is currently within your budget.")

    # -----------------------------------------------------
    # CATEGORY SUMMARY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Expense by Category</div>',
        unsafe_allow_html=True
    )

    category_total = (
        data.groupby("Category")["Price"]
        .sum()
        .sort_values(ascending=False)
    )

    category_percentage = (
        category_total / total_expense
    ) * 100

    category_table = pd.DataFrame({
        "Total": category_total,
        "Percentage": category_percentage
    })

    st.dataframe(
        category_table.style.format({
            "Total": "₱{:,.2f}",
            "Percentage": "{:.2f}%"
        }),
        use_container_width=True
    )

    # -----------------------------------------------------
    # RECENT EXPENSES
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🧾 Recent Expenses</div>',
        unsafe_allow_html=True
    )

    recent = data.sort_values(
        "Date",
        ascending=False
    ).head(8)

    st.dataframe(
        recent,
        hide_index=True,
        use_container_width=True
    )


# =========================================================
# EXPENSES PAGE
# =========================================================

elif menu == "🧾 Expenses":

    st.title("🧾 Expense Records")

    st.write(
        "Add, view, and remove your personal expense records."
    )

    # -----------------------------------------------------
    # ADD EXPENSE
    # -----------------------------------------------------

    st.subheader("➕ Record New Expense")

    c1, c2, c3 = st.columns(3)

    with c1:
        expense_name = st.text_input("Expense")

    with c2:
        category = st.selectbox(
            "Category",
            [
                "Food",
                "Fare",
                "Drinks",
                "Clothes",
                "Hygiene",
                "Accessories",
                "Laundry",
                "School",
                "Entertainment",
                "Other"
            ]
        )

    with c3:
        source = st.text_input("Source")

    c4, c5 = st.columns(2)

    with c4:
        price = st.number_input(
            "Price",
            min_value=0.0,
            step=1.0
        )

    with c5:
        expense_date = st.date_input(
            "Date"
        )

    if st.button(
        "➕ Record Expense",
        use_container_width=True
    ):

        if expense_name.strip() == "":
            st.warning("Please enter the expense name.")

        elif source.strip() == "":
            st.warning("Please enter the source.")

        elif price <= 0:
            st.warning("Price must be greater than zero.")

        else:

            new_row = pd.DataFrame([
                {
                    "Expense": expense_name,
                    "Category": category,
                    "Source": source,
                    "Price": price,
                    "Date": pd.to_datetime(expense_date)
                }
            ])

            data = pd.concat(
                [data, new_row],
                ignore_index=True
            )

            data.to_csv(
                "personalexpense.csv",
                index=False
            )

            st.success("✅ Expense successfully recorded!")

            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # DELETE EXPENSE
    # -----------------------------------------------------

    st.subheader("🗑️ Manage Expenses")

    editable_data = data.copy()

    editable_data["Delete"] = False

    edited_data = st.data_editor(
        editable_data,
        num_rows="fixed",
        hide_index=True,
        use_container_width=True
    )

    if st.button(
        "🗑️ Remove Selected",
        use_container_width=True
    ):

        remaining_data = edited_data[
            edited_data["Delete"] == False
        ].drop(columns=["Delete"])

        remaining_data.to_csv(
            "personalexpense.csv",
            index=False
        )

        st.success("Selected records removed!")

        st.rerun()


# =========================================================
# ANALYTICS PAGE
# =========================================================

elif menu == "📊 Analytics":

    st.title("📊 Expense Analytics")

    st.write(
        "Analyze how your money is being spent."
    )

    # -----------------------------------------------------
    # TOTAL AND PERCENTAGE
    # -----------------------------------------------------

    st.subheader("💸 Expense Distribution")

    category_total = (
        data.groupby("Category")["Price"]
        .sum()
        .sort_values(ascending=False)
    )

    category_percentage = (
        category_total / total_expense
    ) * 100

    c1, c2 = st.columns(2)

    with c1:

        st.write("### Total by Category")

        category_display = pd.DataFrame({
            "Category": category_total.index,
            "Total": category_total.values,
            "Percentage": category_percentage.values
        })

        st.dataframe(
            category_display.style.format({
                "Total": "₱{:,.2f}",
                "Percentage": "{:.2f}%"
            }),
            hide_index=True,
            use_container_width=True
        )

    # -----------------------------------------------------
    # MATPLOTLIB CATEGORY CHART
    # -----------------------------------------------------

    with c2:

        fig, ax = plt.subplots()

        ax.bar(
            category_total.index,
            category_total.values
        )

        ax.set_title("Expenses by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₱)")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    # -----------------------------------------------------
    # DAILY SPENDING
    # -----------------------------------------------------

    st.subheader("📅 Daily Spending Trend")

    daily_total = (
        data.groupby("Date")["Price"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots()

    ax.plot(
        daily_total.index,
        daily_total.values,
        marker="o"
    )

    ax.set_title("Daily Expense Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount (₱)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# =========================================================
# BUDGET PAGE
# =========================================================

elif menu == "💰 Budget":

    st.title("💰 Budget Tracker")

    st.write(
        "Monitor your spending against your available budget."
    )

    # -----------------------------------------------------
    # BUDGET SUMMARY
    # -----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Monthly Budget",
            f"₱{budget:,.2f}"
        )

    with c2:
        st.metric(
            "Monthly Expenses",
            f"₱{monthly_total:,.2f}"
        )

    with c3:

        st.metric(
            "Remaining",
            f"₱{remaining_budget:,.2f}"
        )

    st.divider()

    # -----------------------------------------------------
    # BUDGET PROGRESS
    # -----------------------------------------------------

    st.subheader("📊 Budget Usage")

    progress = min(
        max(monthly_total / budget, 0),
        1
    ) if budget > 0 else 0

    st.progress(progress)

    st.write(
        f"You have used **{budget_percentage:.2f}%** "
        f"of your monthly budget."
    )

    if budget_percentage >= 100:

        st.error(
            "🚨 Budget exceeded!"
        )

    elif budget_percentage >= 80:

        st.warning(
            "⚠️ You are close to reaching your budget."
        )

    else:

        st.success(
            "✅ You are within your budget."
        )

    # -----------------------------------------------------
    # TOP EXPENSE
    # -----------------------------------------------------

    st.subheader("💸 Highest Expense")

    highest_row = data.loc[
        data["Price"].idxmax()
    ]

    st.info(
        f"**{highest_row['Expense']}** — "
        f"₱{highest_row['Price']:,.2f} "
        f"({highest_row['Category']})"
    )

    # -----------------------------------------------------
    # SCIPY ANALYSIS
    # -----------------------------------------------------

    st.subheader("🔎 Spending Pattern Analysis")

    if len(data) >= 2:

        expense_prices = data["Price"].to_numpy()

        mean_price = np.mean(expense_prices)

        std_price = np.std(
            expense_prices,
            ddof=1
        )

        if std_price > 0:

            highest_z = (
                highest_expense - mean_price
            ) / std_price

            if highest_z >= 2:

                st.warning(
                    "Your highest expense is considerably "
                    "higher than your typical expense."
                )

            else:

                st.success(
                    "Your highest expense is within the "
                    "general range of your recorded expenses."
                )

            st.write(
                f"Average expense: **₱{mean_price:,.2f}**"
            )

            st.write(
                f"Standard deviation: **₱{std_price:,.2f}**"
            )

            st.write(
                f"Highest expense z-score: **{highest_z:.2f}**"
            )

        else:

            st.info(
                "There is not enough variation in your "
                "expenses for statistical analysis."
            )

    else:

        st.info(
            "Add more expenses to perform statistical analysis."
        )
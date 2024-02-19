import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

# Custom CSS for styling to resemble Telegram and additional styling provided
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #eff0f4;
    }
    .stApp header, .stApp footer {
        background-color: #0088cc;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #eff0f4;
    }
    .css-2trqyj, .css-rli0r1, .css-1h5w3w5 {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: none;
    }
    .css-1eh6y2u {
        padding: 1rem;
    }
    .css-1eh6y2u .st-cq .st-da {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .css-1eh6y2u .st-cq .st-eu {
        padding: 1rem;
    }
    .css-1eh6y2u .st-cq .st-eu .st-et {
        margin-top: 1rem;
    }
    .css-1eh6y2u .st-dm {
        max-width: 1200px;
        margin: auto;
    }
    /* Additional CSS styling */
    [data-testid="block-container"] {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-bottom: -7rem;
    }
    [data-testid="stVerticalBlock"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    [data-testid="stMetric"] {
        background-color: #393939;
        text-align: center;
        padding: 15px 0;
    }
    [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    [data-testid="stMetricDeltaIcon-Up"],
    [data-testid="stMetricDeltaIcon-Down"] {
        position: relative;
        left: 38%;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        transform: translateX(-50%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to validate login credentials
def authenticate(username, password):
    return username == "Admin" and password == "Admin123"

# Login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password. Please try again.")

# Function to display balance sheet
def display_balance_sheet():
    balance_sheet_data = {
        "Current Assets": {
            "Cash": st.number_input("Current Assets - Cash", value=3000),
            "Accounts Receivable": st.number_input("Current Assets - Accounts Receivable", value=18892),
            "Merchandise Inventory": st.number_input("Current Assets - Merchandise Inventory", value=18000),
            "Prepaid Expenses": st.number_input("Current Assets - Prepaid Expenses", value=0),
            "Notes Receivable": st.number_input("Current Assets - Notes Receivable", value=0)
        },
        "Fixed Assets": {
            "Vehicles": st.number_input("Fixed Assets - Vehicles", value=0),
            "Furniture and Fixtures": st.number_input("Fixed Assets - Furniture and Fixtures", value=0),
            "Equipment": st.number_input("Fixed Assets - Equipment", value=-500),
            "Buildings": st.number_input("Fixed Assets - Buildings", value=0),
            "Land": st.number_input("Fixed Assets - Land", value=0)
        },
        "Other Assets": {
            "Goodwill": st.number_input("Other Assets - Goodwill", value=0)
        },
        "Current Liabilities": {
            "Accounts Payable": st.number_input("Current Liabilities - Accounts Payable", value=500),
            "Sales Taxes Payable": st.number_input("Current Liabilities - Sales Taxes Payable", value=0),
            "Payroll Taxes Payable": st.number_input("Current Liabilities - Payroll Taxes Payable", value=0),
            "Accrued Wages Payable": st.number_input("Current Liabilities - Accrued Wages Payable", value=0),
            "Unearned Revenues": st.number_input("Current Liabilities - Unearned Revenues", value=0),
            "Short-Term Notes Payable": st.number_input("Current Liabilities - Short-Term Notes Payable", value=500),
            "Short-Term Bank Loan Payable": st.number_input("Current Liabilities - Short-Term Bank Loan Payable", value=0)
        },
        "Long-Term Liabilities": {
            "Long-Term Notes Payable": st.number_input("Long-Term Liabilities - Long-Term Notes Payable", value=0),
            "Mortgage Payable": st.number_input("Long-Term Liabilities - Mortgage Payable", value=0)
        },
        "Capital": {
            "Owner's Equity": st.number_input("Capital - Owner's Equity", value=0),
            "Net Profit": st.number_input("Capital - Net Profit", value=38392)
        }
    }

    # Creating DataFrame from balance sheet data
    df_balance_sheet = pd.DataFrame(balance_sheet_data).fillna(0)

    # Display the balance sheet
    st.write("<h2 style='text-align:center'>Balance Sheet</h2>", unsafe_allow_html=True)

    # Display tables side by side using Streamlit columns
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Assets")
        st.write(df_balance_sheet.iloc[:, :3])
    with col2:
        st.write("## Liabilities and Capital")
        st.write(df_balance_sheet.iloc[:, 3:])

    # Display total assets
    total_assets = df_balance_sheet["Current Assets"].sum() + df_balance_sheet["Fixed Assets"].sum() + df_balance_sheet["Other Assets"].sum()
    st.write(f"Total Assets: ${total_assets}")

    # Display total liabilities
    total_liabilities = df_balance_sheet["Current Liabilities"].sum() + df_balance_sheet["Long-Term Liabilities"].sum()
    st.write(f"Total Liabilities: ${total_liabilities}")

    # Display total capital
    total_capital = df_balance_sheet["Capital"].sum()
    st.write(f"Total Capital: ${total_capital}")

    # Display total liabilities and capital
    total_liabilities_capital = total_liabilities + total_capital
    st.write(f"Total Liabilities and Capital: ${total_liabilities_capital}")

    # Check if all values are zero, which would cause ValueError
    if total_assets == 0 or total_liabilities_capital == 0:
        st.warning("No data to display in pie charts.")
        return

    # Plot histograms and pie charts
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Histogram for total assets
    asset_colors = ['#4db8ff', '#ffb84d', '#99ff99']
    axes[0, 0].bar(df_balance_sheet.columns[:3], df_balance_sheet.sum()[:3], color=asset_colors)
    axes[0, 0].set_title('Total Assets', fontsize=18)
    axes[0, 0].set_xlabel('Asset Type', fontsize=14)
    axes[0, 0].set_ylabel('Amount ($)', fontsize=14)
    axes[0, 0].tick_params(axis='x', labelsize=12)
    axes[0, 0].tick_params(axis='y', labelsize=12)

    # Histogram for total liabilities
    liability_colors = ['#ff6347', '#d32f2f', '#b71c1c', '#d9e6f2', '#a5c6e8']
    axes[0, 1].bar(df_balance_sheet.columns[3:], df_balance_sheet.sum()[3:], color=liability_colors)
    axes[0, 1].set_title('Total Liabilities', fontsize=18)
    axes[0, 1].set_xlabel('Liability Type', fontsize=14)
    axes[0, 1].set_ylabel('Amount ($)', fontsize=14)
    axes[0, 1].tick_params(axis='x', labelsize=12)
    axes[0, 1].tick_params(axis='y', labelsize=12)

    # Pie chart for asset composition
    assets_data = df_balance_sheet.iloc[:, :3].sum()
    assets_data = assets_data[assets_data > 0]  # Exclude zero or negative values
    axes[1, 0].pie(assets_data, labels=assets_data.index, autopct='%1.1f%%', startangle=90, colors=asset_colors)
    axes[1, 0].axis('equal')
    axes[1, 0].set_title('Asset Composition', fontsize=18)

    # Pie chart for liability and capital composition
    liabilities_data = df_balance_sheet.iloc[:, 3:].sum()
    liabilities_data = liabilities_data[liabilities_data > 0]  # Exclude zero or negative values
    axes[1, 1].pie(liabilities_data, labels=liabilities_data.index, autopct='%1.1f%%', startangle=90, colors=liability_colors)
    axes[1, 1].axis('equal')
    axes[1, 1].set_title('Liability and Capital Composition', fontsize=18)

    plt.tight_layout()
    st.pyplot(fig)

# Main function
def main():
    if not st.session_state.get('logged_in'):
        login()
    else:
        # Add dark mode toggle
        dark_mode = st.sidebar.checkbox("Dark Mode")
        
        # Add WhatsApp profile picture and name
        st.sidebar.image("Tasha.png", width=100, use_column_width='auto')
        st.sidebar.write("Tasha")
        
        # Add bio under the image
        st.sidebar.write("assistant Bot")
        
        if dark_mode:
            # Set dark mode theme
            st.markdown("""
            <style>
            body {
                color: orange;
                background-color: black;
            }
            .stApp header, .stApp footer {
                background-color: orange;
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Add logout button
        if st.sidebar.button("Logout" if st.session_state.get('logged_in') else "Login"):
            st.session_state['logged_in'] = not st.session_state.get('logged_in')

        if st.session_state.get('logged_in'):
            display_balance_sheet()

if __name__ == "__main__":
    main()


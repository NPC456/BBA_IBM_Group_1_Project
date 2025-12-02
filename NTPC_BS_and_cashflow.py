import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

balance_sheet_file = "NTPC_Balancesheet_2025.csv"
balance_sheet = pd.read_csv(balance_sheet_file)

# Assets are in the first two columns
assets = balance_sheet[['Asset', 'Amount']].dropna(subset=['Asset'])
assets.columns = ['Category', 'Amount']

# Liabilities are in the last two columns
liabilities = balance_sheet[['Liabilities', 'Amount']].dropna(subset=['Liabilities'])
liabilities.columns = ['Category', 'Amount']

# Load Cashflow data
cashflow_file = "NTPC_CashFlow_2025.csv"
cashflow = pd.read_csv(cashflow_file)
cashflow = cashflow.rename(columns={cashflow.columns[0]: 'Activity'})
cashflow = cashflow[cashflow['Activity'].notna()]

# Convert cashflow values to numeric
for col in cashflow.columns[1:]:
    cashflow[col] = pd.to_numeric(cashflow[col], errors='coerce')

colors_assets = ["#FE3232", "#00FFEE", "#0BFF69", "#FFF93F"]
colors_liabilities = ["#1A7DFF", "#FF0404", "#7D49F6", "#F11267", "#1ABE22"]
activity_colors = {
    'Operating Activities': '#00B050',
    'Investing Activities': '#FF0000',
    'Financing Activities': '#FFC000'
}

fig = plt.figure(figsize=(14, 10))

# Create grid for subplots
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

# Assets Pie Chart
ax1.pie(assets['Amount'], labels=assets['Category'], autopct='%1.1f%%', startangle=140, colors=colors_assets, shadow=True, explode=[0.05]*len(assets))
ax1.set_title("NTPC Balance Sheet (2025) - Assets", fontsize=12, fontweight='bold')

# Liabilities Pie Chart
ax2.pie(liabilities['Amount'], labels=liabilities['Category'], autopct='%1.1f%%', startangle=140, colors=colors_liabilities, shadow=True, explode=[0.05]*len(liabilities))
ax2.set_title("NTPC Balance Sheet (2025) - Liabilities", fontsize=12, fontweight='bold')

# Cashflow Bar Chart with positive and negative values
years = list(cashflow.columns[1:])
x = range(len(years))
width = 0.25

activities = cashflow['Activity'].tolist()

for i, activity in enumerate(activities):
    values = cashflow.iloc[i, 1:].values
    color = activity_colors.get(activity, '#000000')
    x_pos = [p + (width * (i - 1)) for p in x]
    bars = ax3.bar(x_pos, values, width, label=activity, color=color)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

ax3.set_title("NTPC Cashflow (2020-2025)", fontsize=12, fontweight='bold')
ax3.set_ylabel("Amount (in Crores)", fontsize=10)
ax3.set_xlabel("Fiscal Year", fontsize=10)
ax3.set_xticks(x)
ax3.set_xticklabels(years)
ax3.legend(loc='upper right', fontsize=10)
ax3.grid(axis='y', alpha=0.3)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

plt.subplots_adjust(top=0.96, bottom=0.08)
plt.show()

# Displaying the balance sheet data
print("Assets:")
print(assets)
print(f"\nTotal Assets: {assets['Amount'].sum()}")
print("\nLiabilities:")
print(liabilities)
print(f"\nTotal Liabilities: {liabilities['Amount'].sum()}")
print("\nCashflow Data:")
print(cashflow)

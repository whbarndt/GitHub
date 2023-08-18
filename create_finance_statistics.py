import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import sys
import yaml

# Specify the path to the YAML file
yaml_file_path = 'config.finance.yml'

# Open and read the YAML file
with open(yaml_file_path, 'r') as file:
    yaml_data = yaml.safe_load(file)

# Load data from YAML file
year = yaml_data['Year']
path_to_expense_dir = yaml_data['Expenses_path']

# Read Expense File and convert 'Date' to datetime
expense_file = f'{year}-Expense-Report.csv'
expense_df = pd.read_csv(path_to_expense_dir + expense_file, comment='#')
expense_df['Date'] = pd.to_datetime(expense_df['Date'])

# Get Unique Businesses, Locations and Tags
locations = expense_df['Location'].unique()
businesses = expense_df['Business'].unique()
unique_grouped_tags = expense_df['Tags'].unique()
all_tags = '/'.join(expense_df['Tags']).split('/')
unique_individual_tags = set(all_tags)
tags_for_stats = ['Groceries', 'Snacks', 'Meal', 'Coffee', 'Entertainment', 'Membership']

# Create Statistics Dataframe
stats_df = pd.DataFrame()

# Statistics Column Headers
column_headers = ['Month', 'Total_Expenses']
for tag in tags_for_stats:
    column_headers.append(f'{tag}_Expenses')

# Grab months from expense report
months_in_expenses = expense_df['Date'].dt.strftime("%m").unique().tolist()

# Create stat rows 
for month_num_str in months_in_expenses:
    row_stats = {}
    month_num = int(month_num_str)
    row_stats['Month'] = month_num
    month_expenses = expense_df[expense_df['Date'].dt.month == month_num]
    row_stats['Total_Expenses'] = month_expenses['Cost'].sum()
    for tag in tags_for_stats:
        tag_month_expense = month_expenses[month_expenses['Tags'].str.contains(tag, case=False, na=False)]
        row_stats[f'{tag}_Expenses'] = tag_month_expense['Cost'].sum()
    row_stats_df = pd.DataFrame([row_stats])
    stats_df = pd.concat([stats_df, row_stats_df])
stats_df.set_index('Month', inplace=True)
print(stats_df)

# Stats Visualization
sns.set_theme()

plt.figure(figsize=[12, 8])
ax = sns.lineplot(data=stats_df.drop(columns=['Total_Expenses']), markers=True)

plt.title(f"{year} Expenses by Month")
plt.xlabel("Months")
plt.ylabel("Expense Cost ($)")

plt.savefig(f"{year}_Tag_Expenses.png")

'''plt, ax = plt.subplots(figsize=[12,8])
ax.set_title(f"{year} Expenses by Month")
ax.set_xlabel("Months")
ax.set_ylabel("Expense Cost ($)")
stats_df_no_total = stats_df.drop(columns=['Total_Expenses'])
stats_df_no_total.plot(ax=ax)
plt.savefig(f"{year}_Tag_Expenses.png")'''
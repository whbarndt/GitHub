import numpy as np
import pandas as pd
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

# Create Statistics Dataframe
stats_df = pd.DataFrame()

# Grab months from expense report
column_headers = ['Month', 'Total_Expenses', 'Grocery_Expenses', 'Snack_Expenses', 'Coffee_Expenses']
months_in_expenses = expense_df.groupby(expense_df['Date'].dt.to_period('M'))
for month_num in months_in_expenses:
    row_stats = []
    row_stats.append(month_num)
    month_expenses = expense_df[expense_df['Date'].dt.month == month_num]
    row_stats.append(month_expenses['Cost'].sum())
    '''for tag in tags:
        tag_month_expense = month_expenses[month_expenses['Tags'].str.contains(tag, case=False, na=False)]
        tag_cost = tag_month_expense['Cost'].sum()
        stats_df[f'{tag}_Expenses'] = tag_cost'''
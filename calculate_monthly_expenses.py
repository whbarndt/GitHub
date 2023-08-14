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
expense_file = f'{year}-Expenses.csv'
expense_df = pd.read_csv(path_to_expense_dir + expense_file, comment='#')
expense_df['Date'] = pd.to_datetime(expense_df['Date'])

# Get month expenses
while True:
    print("Which month would you like to see total expenses from?: [Options: 1 - 12]")
    month_of_choice = input("Type 'quit' to quit\n")
    if int(month_of_choice) >= 1 and int(month_of_choice) <= 12:
        month_of_choice = int(month_of_choice)
        break
    elif month_of_choice == 'quit':
        sys.exit()
    else:
        print("Error: Please choose a valid month number")

# Total Expenses for Month
month_expenses = expense_df[expense_df['Date'].dt.month == month_of_choice]
month_cost = month_expenses['Cost'].sum()
print(f"Month {month_of_choice} Expenses: {month_cost}")

# Calculate Total expenses for a Tag
print("Which tag from the month would you like to see total expenses from?: [Options: Look at list...]")
tag_of_choice = input("Type 'quit' to quit\n")
    
tag_month_expense = month_expenses[month_expenses['Tags'].str.contains(tag_of_choice, case=False, na=False)]
tag_cost = tag_month_expense['Cost'].sum()
print(f"Tag Expenses for month of {month_of_choice}: {tag_cost}")


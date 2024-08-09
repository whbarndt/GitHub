import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import sys
import yaml
from pathlib import Path

def main():
    # Open and read the YAML file
    yaml_file_path = Path('config.local.finance.yml')
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    year = yaml_data['Year']
    working_dir = yaml_data['Working_Dir']

    # Read Expense File and convert 'Date' to datetime
    expense_file = f'{year}-Expense-Report.csv'
    expense_df = pd.read_csv(working_dir + expense_file, comment='#')
    expense_df['Date'] = pd.to_datetime(expense_df['Date'])

    # Get Unique Businesses, Locations and Tags
    locations = expense_df['Location'].unique()
    businesses = expense_df['Business'].unique()
    unique_grouped_tags = expense_df['Tags'].unique()
    all_tags = '/'.join(expense_df['Tags']).split('/')
    unique_individual_tags = set(all_tags)
    tags_for_stats = ['Groceries', 'Snacks', 'Meal', 'Drinks', 'Coffee', 'Recreation_&_Entertainment', 'Games', 'Membership', 'Transportation', 'Gifts']
    stack_tags_drop = ['Games_Expenses', 'Coffee_Expenses']

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
    stats_df = stats_df.set_index('Month')
    print(stats_df)
    stats_df.to_csv(f"{year}_Expenses.csv")

    # Stats Visualization
    sns.set_theme(style='darkgrid')
    stats_df_no_total = stats_df.drop(columns=['Total_Expenses'])

    # Line Plot
    fig, ax = plt.subplots(figsize=[12,8])
    stats_df_no_total.plot(ax=ax)
    ax.set_title(f"{year} Expenses by Month")
    ax.set_xlabel("Months")
    ax.set_ylabel("Expense Cost ($)")
    plt.savefig(f"{year}_Tag_Expenses.png")

    # Stacked Plot
    stats_df_no_total = stats_df_no_total.drop(columns=stack_tags_drop)

    fig_2, ax_2 = plt.subplots(figsize=[12, 8])
    stats_df_no_total.plot.area(ax=ax_2)
    ax_2.set_title(f"{year} Expenses by Month")
    ax_2.set_xlabel("Months")
    ax_2.set_ylabel("Expense Cost ($)")
    plt.savefig(f"{year}_Tag_Expenses_Stacked.png")

main()
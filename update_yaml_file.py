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

# Read Expense File
expense_file = f'{year}-Expense-Report.csv'
expense_df = pd.read_csv(path_to_expense_dir + expense_file, comment='#')

# Get Unique Businesses, Locations and Tags from YAML file
yaml_locations = yaml_data['Location']
yaml_businesses = yaml_data['Business']

# Get Unique Businesses, Locations and Tags from .csv file
report_locations = expense_df['Location'].unique()
report_businesses = expense_df['Business'].unique()
report_unique_grouped_tags = expense_df['Tags'].unique()
report_all_tags = '/'.join(expense_df['Tags']).split('/')
report_unique_individual_tags = set(report_all_tags)

# Append both lists and get unique values from it
all_locations = yaml_data['Location'].extend(report_locations)
all_businesses = yaml_data['Business'].extend(report_businesses)
all_unique_locations = all_locations.unique()
all_unique_businesses = all_businesses.unique()

# Replace yaml data with updated data
yaml_data['Location'] = all_unique_locations
yaml_data['Business'] = all_unique_businesses

# Write the updated data back to the YAML file
with open(yaml_file_path, 'w') as file:
    yaml.dump(yaml_data, file)
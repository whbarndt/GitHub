import numpy as np
import pandas as pd
import datetime as dt
import sys
import yaml

# Specify the path to the YAML file
config_yaml_file_path = 'config.finance.yml'
businesses_yaml_file_path = 'businesses.finance.yml'

# Open and read the YAML files
with open(config_yaml_file_path, 'r') as file:
    yaml_data = yaml.safe_load(file)
with open(businesses_yaml_file_path, 'r') as file:
    yaml_data_b = yaml.safe_load(file)

# Load data from YAML file
year = yaml_data['Year']
path_to_expense_dir = yaml_data['Expenses_path']

# Read Expense File
expense_file = f'{year}-Expense-Report.csv'
expense_df = pd.read_csv(path_to_expense_dir + expense_file, comment='#')

# Get Unique Businesses, Locations and Tags from YAML file
yaml_locations = yaml_data['Locations']
yaml_businesses = list(yaml_data['Businesses'].keys())
yaml_tags = yaml_data['Tags']

# Get Unique Businesses, Locations and Tags from .csv file
report_locations = expense_df['Location'].unique()
report_businesses = expense_df['Business'].unique()
report_unique_tags = expense_df['Tags'].unique()
report_all_tags = '/'.join(expense_df['Tags']).split('/')
report_unique_individual_tags = list(set(report_all_tags))

# Append both lists and get unique values from it
yaml_locations.extend(report_locations)
yaml_businesses.extend(report_businesses)
yaml_tags.extend(report_unique_individual_tags)
all_unique_locations = list(set(yaml_locations))
all_unique_businesses = list(set(yaml_businesses))
all_unique_individual_tags = list(set(yaml_tags))

# Sort and Replace yaml data with updated data
np.sort(all_unique_locations)
np.sort(all_unique_businesses)
np.sort(all_unique_individual_tags)

# Replace Locations and Tags
yaml_data['Locations'] = all_unique_locations
yaml_data['Tags'] = all_unique_individual_tags
yaml_data['Businesses'] = all_unique_businesses

# Get all optional tags for businesses from expense report and replace businesses tags
all_buissnesses = {}
for buisness in all_unique_businesses:
    all_business_tags = []
    all_business_locs = []
    expense_business_rows = expense_df[expense_df['Business'] == buisness]
    for tags in expense_business_rows['Tags'].unique():
        all_business_tags.append(tags)
    for loc in expense_business_rows['Location'].unique():
        all_business_locs.append(loc)
    all_buissnesses[buisness] = {'Tags' : all_business_tags, 'Locations' : all_business_locs}
yaml_data_b['Businesses'] = all_buissnesses

# Write the updated data back to the YAML file
with open(config_yaml_file_path, 'w') as file:
    yaml.dump(yaml_data, file, sort_keys=False)
with open(businesses_yaml_file_path, 'w') as file:
    yaml.dump(yaml_data_b, file)
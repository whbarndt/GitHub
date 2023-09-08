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
    config_yaml = yaml.safe_load(file)
with open(businesses_yaml_file_path, 'r') as file:
    businesses_yaml = yaml.safe_load(file)

# Load data from config file
year = config_yaml['Year']
path_to_expense_dir = config_yaml['Expenses_path']

# Read Expense File
expense_file = f'{year}-Expense-Report.csv'
expense_df = pd.read_csv(path_to_expense_dir + expense_file, comment='#')

# Get Unique Businesses, Locations and Tags from config file
config_locations = config_yaml['Locations']
config_businesses = config_yaml['Businesses']
config_tags = config_yaml['Tags']

# Get Unique Businesses, Locations and Tags from .csv file
report_locations = expense_df['Location'].unique()
report_businesses = expense_df['Business'].unique()
report_unique_tags = expense_df['Tags'].unique()
report_all_tags = '/'.join(list(report_unique_tags)).split('/')
report_unique_individual_tags = list(set(report_all_tags))

# Append both lists and get unique values from it
config_locations.extend(report_locations)
config_businesses.extend(report_businesses)
config_tags.extend(report_unique_individual_tags)
all_unique_locations = list(set(config_locations))
all_unique_businesses = list(set(config_businesses))
all_unique_individual_tags = list(set(config_tags))

# Sort and Replace config data with updated data
np.sort(all_unique_locations)
np.sort(all_unique_businesses)
np.sort(all_unique_individual_tags)
config_yaml['Locations'] = all_unique_locations
config_yaml['Tags'] = all_unique_individual_tags
config_yaml['Businesses'] = all_unique_businesses

# Get all optional locations and tags for businesses from expense report and replace existing ones
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
businesses_yaml['Businesses'] = all_buissnesses

# Write the updated data back to the YAML file
with open(config_yaml_file_path, 'w') as file:
    yaml.dump(config_yaml, file, sort_keys=False)
with open(businesses_yaml_file_path, 'w') as file:
    yaml.dump(businesses_yaml, file)
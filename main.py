import json
import time
import os
import requests
import pandas as pd


from datetime import datetime
from data_utils import fetch_data, get_earliest_time, fetch_and_get_earliest_time
from utils import welcome_message, get_workspace_id
from fetch_history import getDate_FNToLDC

# -------- Config -------
# Load configurations from the config.json file
with open('config.json', 'r') as f:
    config = json.load(f)


# -------- Main --------
# Load the cookies from the file
with open(config['file_names']['cookie_file'], 'r') as f:
    cookie_list = json.load(f)

# -------- Welcome message & Config --------
welcome_message()
workspace_id = get_workspace_id()


# -------- Read the excel file --------
# Assuming your excel file is named 'input.xlsx' and is in the same directory as this script
# Read the excel file
df = pd.read_excel(config['file_names']['input_file'])

# Get the ID range from the user
id_start = int(input("请填入需要查询的起始ID (i.e. 1001705) Please enter the starting ID: "))
id_end = int(input("请填入需要查询的结束ID (i.e. 1001800)Please enter the ending ID: "))

# Filter the dataframe based on the given ID range
df = df[(df['ID'] >= id_start) & (df['ID'] <= id_end)]

# -------- Add 响应时间 column to the dataframe --------
# Iterate over each ID in the dataframe
for i, row in df.iterrows():
    entity_id = str(row['ID'])
    earliest_time = fetch_and_get_earliest_time(workspace_id, entity_id, cookie_list, fallback_date=row['完成时间'])
    done_time = getDate_FNToLDC(workspace_id, entity_id, cookie_list)

    # Add the earliest time to the '响应时间' column of the current row
    df.loc[i, '响应时刻'] = earliest_time
    df.loc[i, '完成时刻'] = done_time

    # Convert date to string if earliest_time is not None
    if earliest_time is not None:
        try :
            earliest_time_str = earliest_time.strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError:
            earliest_time_str = 'N/A'

        df.loc[i, '响应时刻_str'] = earliest_time_str
    else:
        df.loc[i, '响应时刻_str'] = 'N/A'

    # Print a success message
    print(f"{entity_id} completed, processing next request...")

    # Pause for a while to avoid hitting API rate limits
    # The sleep time
    time.sleep(3)


# Save the updated dataframe to a new excel file
df.to_excel(f"output/output_raw.xlsx")

# -------- Add additional columns --------
# Convert '创建时间' and '完成时间' to datetime format if they are not
df['创建时间'] = pd.to_datetime(df['创建时间'])
df['完成时间'] = pd.to_datetime(df['完成时间'])
df['响应时刻'] = pd.to_datetime(df['响应时刻'])
df['完成时刻'] = pd.to_datetime(df['完成时刻'])
# Calculate the time differences
df['响应时间_diff'] = df['响应时刻'] - df['创建时间']
df['解决时间_diff'] = df['完成时刻'] - df['创建时间']

# Convert timedelta to "Hour:Minute" string
df['响应时间_diff'] = df['响应时间_diff'].apply(lambda x: str(int(x.total_seconds() // 3600)).zfill(2) + ":" + str(int((x.total_seconds() // 60) % 60)).zfill(2) if pd.notnull(x) else 'N/A')
df['解决时间_diff'] = df['解决时间_diff'].apply(lambda x: str(int(x.total_seconds() // 3600)).zfill(2) + ":" + str(int((x.total_seconds() // 60) % 60)).zfill(2) if pd.notnull(x) else 'N/A')

# Split the dataframe into three based on the '优先级' column
df_high = df[df['优先级'] == 'High'].copy()
df_middle = df[df['优先级'] == 'Middle'].copy()
df_low = df[df['优先级'] == 'Low'].copy()


# Set different compliance criteria for each priority level
df_high['响应时间达标'] = df_high['响应时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['high']['response'] else 'N')  # 1 hour = 60 minutes
df_high['解决时间达标'] = df_high['解决时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['high']['resolution'] else 'N')  # 8 hours = 480 minutes

df_middle['响应时间达标'] = df_middle['响应时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['middle']['response'] else 'N')  # 1 hour = 60 minutes
df_middle['解决时间达标'] = df_middle['解决时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['middle']['resolution'] else 'N')  # 24 hours = 1440 minutes

df_low['响应时间达标'] = df_low['响应时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['low']['response'] else 'N') # 1 hour = 60 minutes
df_low['解决时间达标'] = df_low['解决时间_diff'].apply(lambda x: 'Y' if x != 'N/A' and int(x.split(":")[0]) <= config['compliance_criteria']['low']['resolution'] else 'N')  # 72 hours = 4320 minutes

# ---------- Calculating the percentage -----------------
# Define a function to calculate compliance rate (percentage) and format it
def calculate_compliance_rate(df, column_name):
    value_counts = df[column_name].value_counts(normalize=True)
    return "{:.2%}".format(value_counts['Y']) if 'Y' in value_counts else "0.00%"

# Calculate compliance rates for each dataframe and create a new dataframe with these rates
compliance_rates = pd.DataFrame({
    '响应时间达标率(%)': [
                    calculate_compliance_rate(df_high, '响应时间达标'),
                    calculate_compliance_rate(df_middle, '响应时间达标'),
                    calculate_compliance_rate(df_low, '响应时间达标')],
    '解决时间达标率(%)': [
                    calculate_compliance_rate(df_high, '解决时间达标'),
                    calculate_compliance_rate(df_middle, '解决时间达标'),
                    calculate_compliance_rate(df_low, '解决时间达标')]
}, index=['P2', 'P3', 'P4'])

# Append the compliance rates dataframe to the end of each dataframe
df_high = df_high._append(compliance_rates.loc['P2', :], ignore_index=True)
df_middle = df_middle._append(compliance_rates.loc['P3', :], ignore_index=True)
df_low = df_low._append(compliance_rates.loc['P4', :], ignore_index=True)

# create a folder 
if not os.path.exists('output'):
    os.makedirs('output')

# Create a Pandas Excel writer using XlsxWriter as the engine
writer = pd.ExcelWriter(f"output/output_{id_start}_{id_end}.xlsx", engine='xlsxwriter')

# Write the entire dataframe to a sheet named 'ALL'
df.to_excel(writer, sheet_name='ALL', index=False)
# Write each dataframe to a different worksheet
df_high.to_excel(writer, sheet_name='P2', index=False)
df_middle.to_excel(writer, sheet_name='P3', index=False)
df_low.to_excel(writer, sheet_name='P4', index=False)

# Close the Pandas Excel writer and output the Excel file
writer._save()


# if nothing goes wrong, should be succeed
print(f"Success, your output file is 'output_{id_start}_{id_end}.xlsx'")




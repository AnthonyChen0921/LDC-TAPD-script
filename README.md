Readme

Introduction

This script takes an excel file (expected to be named 'test_all.xlsx') as an input, reads the information, and generates an output excel file ('output_{start_id}_{end_id}.xlsx') after performing certain operations on the data.



How to Run the Script

Make sure your input file is named 'test_all.xlsx' and it is in the same directory as the script.
Run the script. It will prompt you to enter a starting ID and ending ID, these should be integer values present in your data. This range of IDs will be used to filter the data.
After processing the data, the script will output an Excel file named 'output_{start_id}_{end_id}.xlsx'. This file will contain the processed data.



What does the script do?

The script reads data from the 'test_all.xlsx' file, filters the data based on the given ID range, adds a '响应时间' column, calculates the response and resolution time difference, splits the data based on the '优先级' column, and finally calculates compliance rates for each priority level.



Requirements
The script requires the following Python libraries to run:

1. pandas
2. requests
3. json
4. time
5. openpyxl (needed for writing to Excel)
Please install these before running the script using pip:


```
pip install pandas requests json time openpyxl

```

To read Excel files, you need to install the xlrd library or openpyxl as well:


```
pip install xlrd openpyxl

```

The script also uses custom modules named 'data_utils' and 'utils'. Ensure these are available in your Python path.


Points to Note

The script pauses for 0.05 seconds after processing each ID to avoid hitting API rate limits.
The script assumes that the input Excel file contains columns named 'ID', '优先级', '创建时间', and '完成时间'.
Ensure 'cookies.json' is in the same directory, which contains the cookies to be used while fetching data.
The script will prompt you for workspace id after displaying a welcome message. Provide the correct id to proceed.



Troubleshooting

If you get an error related to missing modules, please install them using pip and try again.
If you get an error related to file not found, please ensure that the 'test_all.xlsx' and 'cookies.json' files are in the same directory as the script.
If you get an error related to incorrect data, please check your 'test_all.xlsx' file for any anomalies.



Disclaimer
This script is provided as-is, and it may require adjustments based on your specific needs, such as file names, file locations, and specific business logic. Please use it as a reference and modify it as necessary to suit your requirements.
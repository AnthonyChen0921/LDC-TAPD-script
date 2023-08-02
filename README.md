# Readme

## Introduction

Email bot 和 达标率计算脚本，用于自动发送邮件和计算达标率。由于TAPD API还是内测阶段，并且貌似FN也没申请使用，所以目前只能用request模拟登录来获取数据。

## 我要跑需求达标率：
> 1. 打开cmd，cd到这个文件夹
> 2. 把导出的excel文件放到这个文件夹里，改名为input.xlsx
> 3. 运行下面的命令，根据提示输入start_id和end_id改成你要跑的范围, 比如我想看看从1001705到1001800之间的，就先输入1001705，然后回车，再输入1001800，回车(前小后大，不然会报错)
```
python main.py
```
> 4. 等待运行完毕，会在这个文件夹里生成一个output_{start_id}_{end_id}.xlsx的文件，就是你要的结果了
> 5. 还有一个文件是output_raw.xlsx，是增加了响应时间的原始数据，我不太会用excel所以这个文件可以自行随意操作，不影响结果



## How to Run the Script
Make sure your input file is named 'input.xlsx' and it is in the same directory as the script.
Run the script. It will prompt you to enter a starting ID and ending ID, these should be integer values present in your data. This range of IDs will be used to filter the data.

Use the following command to run the script, 这个是算达标率的，想算的时候跑一下下面的命令:

```
python main.py
```

After processing the data, the script will output an Excel file named 'output_{start_id}_{end_id}.xlsx'. This file will contain the processed data.



## What does the script do?
The script reads data from the 'input.xlsx' file, filters the data based on the given ID range, adds a '响应时间' column, calculates the response and resolution time difference, splits the data based on the '优先级' column, and finally calculates compliance rates for each priority level.



## Requirements
The script requires the following Python libraries to run:

1. pandas
2. requests
3. json
4. time
5. openpyxl (needed for writing to Excel)

### Please install these before running the script using pip:

```
pip install pandas requests json time openpyxl
```

### To read Excel files, you need to install the xlrd library or openpyxl as well:

```
pip install xlrd openpyxl
```

The script also uses custom modules named 'data_utils' and 'utils'. Ensure these are available in your Python path.


## Points to Note

The script pauses for 0.05 seconds after processing each ID to avoid hitting API rate limits.
The script assumes that the input Excel file contains columns named 'ID', '优先级', '创建时间', and '完成时间'.
Ensure 'cookies.json' is in the same directory, which contains the cookies to be used while fetching data.
The script will prompt you for workspace id after displaying a welcome message. Provide the correct id to proceed.



# Troubleshooting

## 1. pip install时报错
> Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1002)'

### Solution:
> This issue is occurring because the Python pip installer is unable to verify the SSL certificate of the server it's trying to connect to. This is a common issue when connecting to the internet from a corporate network, which might be using a self-signed certificate for securing its internal connections.

>Install Packages without Certificate Verification: This is the simplest but least secure solution. You can use the --trusted-host option with pip to bypass SSL certificate verification. You should only use this option if you're sure the network connection is secure.

```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas
```

To install other packages, replace "pandas" with "package_name"

## Disclaimer

> This script is provided as-is, and it may require adjustments based on your specific needs, such as file names, file locations, and specific business logic. Please use it as a reference and modify it as necessary to suit your requirements.


Edit by 1nka, If you have further questions, please contact me.
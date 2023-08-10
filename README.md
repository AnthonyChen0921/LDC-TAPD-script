# Readme

## Introduction

Email bot 和 达标率计算脚本，用于自动发送邮件和计算达标率。由于TAPD API还是内测阶段，并且貌似FN也没申请使用，所以目前只能用request模拟登录来获取数据。

btw, i invernted a wheel since TAPD has a built-in feature to send email notifications.

## 环境搭建，安装依赖:
> 1. 安装python环境，开发的版本是3.11.4, 但是3.7以上应该都可以
> 2. 安装依赖，打开cmd，cd到这个文件夹，然后运行下面的命令 (出错请移步Trouble shooting)
```
pip install pandas requests json time openpyxl xlsxwriter datetime logging
```
上面的不行run这个
```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas requests json time openpyxl xlsxwriter datetime logging
```
> 3. 把cookies.json文件放到这个文件夹里，cookies可以在用浏览器登录TAPD后，使用[editThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)插件导出，然后复制进去


## Need Calculation-需求达标率：
> 1. 打开cmd，cd到这个文件夹
> 2. 把TAPD上导出的excel文件放到这个文件夹里，改名为input.xlsx
> 3. 运行下面的命令，根据提示输入start_id和end_id改成你要跑的范围, 比如我想看看从1001705到1001800之间的，就先输入1001705，然后回车，再输入1001800，回车(前小后大，不然会报错)
```
python main.py
```
> 4. 等待运行完毕，会在这个文件夹里生成一个output_{start_id}_{end_id}.xlsx的文件，就是你要的结果了
> 5. 还有一个文件是output_raw.xlsx，是增加了响应时间的原始数据，我不太会用excel所以这个文件可以自行随意操作，不影响结果

## Need run EmailBot-TAPD机器人：
> 1. 打开cmd，cd到这个文件夹
> 2. Run emailbot.py
```
python emailbot.py
```
> 3. emailbot就一直在跑了，不用管它，执行日志会存入emailbot.log文件里，如果有问题可以看日志
> 4. 如果报错退出了，可以重新运行，不会重复发送邮件，会从上次退出的地方继续跑（断电记忆捏）


# Features - 功能 与 执行条件

## Email Bot - 邮件机器人

1. 自动发送邮件, 检测条件是从FN处理中变为LDC确认中时，会给对应的处理人(owner)发一份带链接的邮件。

2. 自动分配处理人，执行条件是如果处理人为空，则自动填入创建人

3. 自动分类Case，执行条件是如果Case分类为未分类，并且标题名字由"Case-"开头，则自动归类生产Case。

### Add-ons - 附加功能 (nice to have)

1. 断档保护，如果程序中断，下次运行会从上次中断的地方继续运行，不会重复发送邮件，并且不会漏发邮件。

2. 日志记录，程序运行时会记录日志，如果有问题可以查看日志。如果某个处理人没有邮件地址，则出现warning，可手动填入contact.json

3. 配置文件，可以在config.json里修改一些数据，见下文：

```
{
    定义了一些文件名，如果你想让程序读新的文件而不删掉旧的文件，把新文件放进来，在这儿改个名字
    "file_names": {
        "cookie_file": "cookies.json", 这是浏览器Cookie，登录TAPD后用editthiscookie导出后直接复制进去，上文有提到
        "input_file": "input.xlsx", 这是你要算解决率，完成时刻，响应时刻，优先级的原始数据，从TAPD上导出来的，ID字段，完成时间字段是required
        "output_folder": "output", 输出文件的名字
        "story_file": "story.json", 可以忽略，程序会自动添加
        "unclassified_story_file": "story_unclassified.json", 同上
        "email_map_file": "contact.json" 这是处理人和email的对应表，map，如果处理人没有email，会出现warning，可以手动添加
    },
    "api": {
        "sleep_time": 10 程序读秒时间，每x秒做一次检测，比对状态，发送邮件，分类Case，填入处理人。可以考虑设置成60s
    },
    "compliance_criteria": {
        "high": {
            "response": 4, 高优先级响应时间要求
            "resolution": 24 高优先级解决时间要求
        },
        "middle": {
            "response": 8, 中优先级响应时间要求
            "resolution": 72 中优先级解决时间要求
        },
        "low": {
            "response": 16, 低优先级响应时间要求
            "resolution": 144 低优先级解决时间要求
        }
    },
    "control_flags": { 一些开关，可以自行设置，1是开，0是关
        "email": 1, 是否发送邮件
        "classify": 1, 是否分类Case
        "autoClose": 0, 是否自动关闭Case
        "autoFillOwner": 1 是否自动填入处理人
    },
    "workspace_id": "55989309", TAPD的workspace id，可以在TAPD上找到（url）
    "threshold_days": 30 天内的Case会被自动关闭
}
```




## How to Run the Script
Make sure your input file is named 'input.xlsx' and it is in the same directory as the script.
Run the script. It will prompt you to enter a starting ID and ending ID, these should be integer values present in your data. This range of IDs will be used to filter the data.

Use the following command to run the script, 

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
This issue is occurring because the Python pip installer is unable to verify the SSL certificate of the server it's trying to connect to. This is a common issue when connecting to the internet from a corporate network, which might be using a self-signed certificate for securing its internal connections.

Install Packages without Certificate Verification: This is the simplest but least secure solution. You can use the --trusted-host option with pip to bypass SSL certificate verification. You should only use this option if you're sure the network connection is secure.

```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas
```

To install other packages, replace "pandas" with "package_name"

## 2. 运行时有warning
> InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.tapd.cn'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings

在data_utils.py里我把request里verify=false了，true的话会报那个SSL，但是false的话会报这个warning，不知道怎么解决，但是不影响结果，所以就先这样吧


## Disclaimer

> This script is provided as-is, and it may require adjustments based on your specific needs, such as file names, file locations, and specific business logic. Please use it as a reference and modify it as necessary to suit your requirements.


Edit by 1nka, If you have further questions, please contact me.
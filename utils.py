# utils.py

import requests
from datetime import datetime

def welcome_message():
    print("TAPD 响应时间查询 & 达标率自动计算工具")
    input("按下回车继续 Press Enter to start...")

def get_workspace_id():
    # Ask for workspace_id
    workspace_id = input("默认按下回车继续 如果无法运行, 请填入WorkspaceID \nPlease enter your workspace ID (or press Enter to use the default workspace ID 55989309): ")
    if workspace_id == "":
        workspace_id = '55989309'
    print(f"Using workspace ID: {workspace_id}")
    return workspace_id



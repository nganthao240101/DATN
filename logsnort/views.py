from django.shortcuts import render
from django.http import JsonResponse
import os
from datetime import datetime
import pandas as pd
import math
from cores.convert_snort import read_snort
from collections import Counter
import json

def read_snort_log(file_path):
    snort_list = read_snort(file_path)
    last_timestamp = max(item['time'] for item in snort_list)
    last_time = datetime.strptime(last_timestamp, "%m/%d-%H:%M:%S.%f") if last_timestamp else None
      # Parse dữ liệu log trước
    filtered_logs = []
    
    for log in snort_list:
        timestamp_str = log['time']
        timestamp = datetime.strptime(timestamp_str, "%m/%d-%H:%M:%S.%f")

        # Lọc các log mới hơn last_timestamp
        if last_time is None or timestamp > last_time:
            filtered_logs.append(log)
    
    return filtered_logs,last_time
def data_snort():
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # file_path = os.path.join(base_dir, 'var/log/snort', 'alert_fast.log')
    file_path="/var/log/snort/alert_fast.log"
    snort_list,last_time = read_snort_log(file_path)
    
    if not snort_list:
        print("No logs found or timestamp format is incorrect.")
    
    return snort_list,last_time

def logsnort_view(request):
    # last_timestamp = request.GET.get('last_timestamp', None)
    # last_time = datetime.strptime(last_timestamp, "%m/%d-%H:%M:%S.%f") if last_timestamp else None
    
    # Lấy dữ liệu từ hàm data_snort
    snort_list,lastest_timestamp= data_snort()
    
    

    # Khởi tạo dữ liệu phản hồi
    response_data = {
        'logs': snort_list,
        'latest_timestamp': None
    }
    
    if snort_list:
        # Cập nhật latest_timestamp
        response_data['latest_timestamp'] = lastest_timestamp
        
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['srcip'] for item in snort_list]
        srcport_list = [item['srcport'] for item in snort_list]
        destport_list = [item['destport'] for item in snort_list]
        
        # Đếm số lần xuất hiện của mỗi giá trị
        srcip_data = dict(Counter(srcip_list))
        destport_data = dict(Counter(destport_list))
        
        # Chuẩn bị dữ liệu cho template
        context = {
            'logs': snort_list,
            'latest_timestamp': lastest_timestamp,
            'labels_srcip': json.dumps(list(srcip_data.keys())),
            'values_srcip': json.dumps(list(srcip_data.values())),
            'labels_port': json.dumps(list(destport_data.keys())),
            'values_port': json.dumps(list(destport_data.values()))   
        }
    else:
        # Nếu không có dữ liệu, cung cấp dữ liệu mặc định
        context = {
            'logs': [],
            'latest_timestamp': None,
            'labels_srcip': json.dumps([]),
            'values_srcip': json.dumps([]),
            'labels_port': json.dumps([]),
            'values_port': json.dumps([])
        }
    
    return render(request, 'logsnort/index.html', context)


def call_logsnort(request):
    snort_list = data_snort()
    if snort_list is not None:
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['srcip'] for item in snort_list]
        srcport_list = [item['srcport'] for item in snort_list]
        destport_list = [item['destport'] for item in snort_list]

        # Đếm số lần xuất hiện của mỗi giá trị
        srcip_count = Counter(srcip_list)
        srcport_count = Counter(srcport_list)
        destport_count = Counter(destport_list)
        return JsonResponse(snort_list,safe=False)




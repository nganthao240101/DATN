from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math,os
from cores.convert_json import csv_to_json
from dateutil import parser
from cores.get_latest_file import get_latest_file
from home.models import RealTimePrediction
from django.forms.models import model_to_dict

def logpcap_view(request):
    return render(request,'logpcap/index.html')

def logpcap_filter(request):
    data_dict = RealTimePrediction.objects.all().values()
    print("test",data_dict)
    print(type(data_dict)) 
    # Chuyển đổi QuerySet thành danh sách từ điển
    # data_list = [model_to_dict(item) for item in data_dict]
    # print(type(data_list))
    # Xử lý dữ liệu
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0

    # Xử lý lọc theo khoảng thời gian
    if request.method == 'GET':
        date_range = request.GET.get('dateRange',None)
        if date_range:
            try:
                start_date_str, end_date_str = date_range.split(' - ')

                
                # Chuyển đổi thành kiểu datetime với định dạng '%m/%d/%Y %I:%M %p'
                start_date = datetime.strptime(start_date_str.strip(), '%m/%d/%Y %I:%M %p')
                end_date = datetime.strptime(end_date_str.strip(), '%m/%d/%Y %I:%M %p')
            except ValueError:
                return JsonResponse({'error': 'Invalid date range format'}, status=400)

            filtered_data = [item for item in data_dict if start_date <= parser.parse(item['timestamp']) <= end_date]
            return JsonResponse({'rows': filtered_data}, safe=False)

    # Trả về 100 bản ghi đầu tiên khi không có dateRange
    first_100_items = data_dict[:1500]

    unique_src_ips = set()
    count = 0
    for item in data_dict:
        src_ip = item.get('Src IP')
        if src_ip not in unique_src_ips:
            unique_src_ips.add(src_ip)
            count += 1
    return JsonResponse({'total': count, 'rows': first_100_items}, safe=False)
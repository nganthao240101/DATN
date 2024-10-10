from django.shortcuts import render
from django.http import JsonResponse
import os
import datetime
import pandas as pd
import math
from cores.convert_pfsense import read_logpfsense
from collections import Counter
import json
from django.contrib.auth.decorators import login_required


def data_pfsense():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'cores', 'log_pfsense')
    pfsense_list = read_logpfsense(file_path)
    return pfsense_list


@login_required
def logpfsense_view(request):
    getdata = data_pfsense()
    pfsense_list = sorted(getdata, key=lambda x: x['timestamp'], reverse=True)
    pfsense_list = pfsense_list[:50]
    if pfsense_list is not None:
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['src_ip'] for item in pfsense_list]
        srcport_list = [item['src_port'] for item in pfsense_list]
        destport_list = [item['dst_port'] for item in pfsense_list]
        
        # Đếm số lần xuất hiện của mỗi giá trị
        data = {
            'srcip_count': dict(Counter(srcip_list)),
            'srcport_count': dict(Counter(srcport_list)),
            'destport_count': dict(Counter(destport_list))
        }
        # srcip_count
        srcip_data = dict(Counter(srcip_list))
        labels_srcip = list(srcip_data.keys())
        values_srcip = list(srcip_data.values())

        # destport_count
        destport_data = dict(Counter(destport_list))
        labels_port = list(destport_data.keys())
        values_port = list(destport_data.values())
        context = {
            'labels_srcip': json.dumps(labels_srcip),
            'values_srcip': json.dumps(values_srcip),
            'labels_port' : json.dumps(labels_port),
            'values_port' : json.dumps(values_port)
        }
    return render(request, 'logpfsense/index.html',context)

def call_logpfsense(request):
    getdata = data_pfsense()
    pfsense_list = sorted(getdata, key=lambda x: x['timestamp'], reverse=True)
    pfsense_list = pfsense_list[:50]
    if pfsense_list is not None:
        # Tạo các danh sách giá trị của "srcip", "srcport", và "destport"
        srcip_list = [item['src_ip'] for item in pfsense_list]
        srcport_list = [item['src_port'] for item in pfsense_list]
        destport_list = [item['dst_port'] for item in pfsense_list]

        # Đếm số lần xuất hiện của mỗi giá trị
        srcip_count = Counter(srcip_list)
        srcport_count = Counter(srcport_list)
        destport_count = Counter(destport_list)
        return JsonResponse(pfsense_list,safe=False)



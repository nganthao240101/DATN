from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math,os
from cores.convert_json import csv_to_json
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
from cores.get_latest_file import get_latest_file
from django.contrib.auth.decorators import login_required
from detect.detect import predic_AE,read_csv_
from detect.convert import pcap_to_csv
from cores.sendmail import send_email
from home.models import EmailFileRecord,EmailNotification
import pandas as pd
from django.utils import timezone
from email.utils import parseaddr

@login_required
def detect_view(request):
    return render(request,'detect/index.html')

def detect_core():
    input_path = "/home/ubuntu/Desktop/aipcap/pcap_log"
    directory_path = "/home/ubuntu/Desktop/aipcap/data_input"
    file=get_latest_file(input_path,"pcap")
    pcap_to_csv(file,directory_path)
    latest_file = get_latest_file(directory_path, "csv")
    new_df=read_csv_(latest_file)
    output=predic_AE(new_df)
    data= output.to_csv(index=False)
    data_dict=csv_to_json(data)

    # Xử lý dữ liệu
    for item in data_dict:
        for key, value in item.items():
            if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                item[key] = None
            elif isinstance(value, int) and (value < 0):
                item[key] = 0
    return data_dict

# @csrf_exempt
# def detect_filter(request):
#     # tải file pcap xử lý
#     if request.method == 'POST' and 'pcap-file' in request.FILES:
#         base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         uploaded_file = request.FILES['pcap-file']
#         save_path = os.path.join(base_dir, 'pcap_log', uploaded_file.name)
        
#         with open(save_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
              
#         data = detect_core()
#         unique_src_ips = []
#         count = 0
        
#         for item in data:  # 'data' là danh sách các từ điển (các record từ logs)
#         # Kiểm tra nếu trường 'Label' tồn tại và bằng 1.0 (số thực)
#             if float(item.get("Label", 0)) == 1.0:
#                 src_ip = item.get('Src IP', None)  # Lấy giá trị của Src IP
#                 dst_ip = item.get('Dst IP', None)  # Lấy giá trị của Dst IP
#                 if src_ip and src_ip not in unique_src_ips:
#                     unique_src_ips.append(src_ip)
#                     count += 1

#                     # Tìm tất cả các người dùng trong cơ sở dữ liệu
#                     # users = EmailFileRecord.objects.all()
                    
#                     # # Tiêu đề email cảnh báo
#                     # subject = "Thông báo cảnh báo từ hệ thống"
                    
#                     # # Tạo nội dung email với thông tin IP nguồn và đích
#                     # body_template = (
#                     #     "Chào {name},\n\n"
#                     #     "Hệ thống đã phát hiện hoạt động bất thường.\n"
#                     #     "Đã phát hiện trinh sát từ IP nguồn: {src_ip} đến IP đích: {dst_ip}.\n\n"
#                     #     "Vui lòng kiểm tra hệ thống để xác minh và xử lý kịp thời."
#                     # )
                    
#                     # # Gửi email đến từng người dùng trong danh sách
#                     # for user in users:
#                     #     # Tạo nội dung email với thông tin chi tiết
#                     #     body = body_template.format(name=user.name, src_ip=src_ip, dst_ip=dst_ip)
#                     #     to_email = user.email  # Lấy email từ database
                        
#                     #     # Gửi email
#                     #     if parseaddr(to_email)[1]:
#                     #         success = send_email(subject, body, [to_email])
#                     #         if success:
#                     #             EmailNotification.objects.create(
#                     #                 email=user.email,
#                     #                 content=body,
#                     #                 timecreate=timezone.now()
#                     #             )
#                     #             print(f"Đã gửi email thành công và lưu lịch sử cho: {user.email}")
#                     #         else:
#                     #             print(f"Không thể gửi email tới: {user.email}")
#                     #     else:
#                     #         print(f"Địa chỉ email không hợp lệ: {to_email}")
#     return JsonResponse({'count': count, 'data': data}, safe=False)

# @csrf_exempt
# def logpcap_filter_time(request):
#     data_dict = detect_core()
#     # Xử lý dữ liệu
#     for item in data_dict:
#         for key, value in item.items():
#             if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
#                 item[key] = None
#             elif isinstance(value, int) and (value < 0):
#                 item[key] = 0
#     # Xử lý lọc theo khoảng thời gian
#     date_range = request.GET.get('daterange-with-time', None)
#     if date_range:
#         try:
#             start_date_str, end_date_str = date_range.split(' - ')
#             start_date = datetime.strptime(start_date_str, '%m/%d/%Y %I:%M %p')
#             end_date = datetime.strptime(end_date_str, '%m/%d/%Y %I:%M %p')
#         except ValueError:
#             return JsonResponse({'error': 'Invalid date range format'}, status=400)

#         filtered_data = [item for item in data_dict if start_date <= parser.parse(item['Timestamp']) <= end_date]
#         return JsonResponse({'rows': filtered_data}, safe=False)

#     # Trả về 100 bản ghi đầu tiên khi không có dateRange
#     first_100_items = data_dict[:1500]

#     unique_src_ips = set()
#     count = 0
#     for item in data_dict:  # data là danh sách các từ điển (như ví dụ của bạn)
#                 # Kiểm tra nếu trường 'Label' tồn tại và bằng 1.0 (số thực)
#                 if float(item.get("Label", 0)) == 1.0:
#                     src_ip = item.get('Src IP', None)  # Lấy giá trị của Src IP, mặc định là None nếu không tồn tại
#                     if src_ip and src_ip not in unique_src_ips:
#                         unique_src_ips.append(src_ip)
#                         count += 1
#     return JsonResponse({'total': count, 'rows': first_100_items}, safe=False)


@csrf_exempt
def detect_filter(request):
    # tải file pcap xử lý
    if request.method == 'POST' and 'pcap-file' in request.FILES:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploaded_file = request.FILES['pcap-file']
        save_path = os.path.join(base_dir, 'pcap_log', uploaded_file.name)
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)      
        data = detect_core()
        unique_src_ips = []
        count = 0
        
        # for item in data:
        #     if float(item.get("Label",0))==1.0:
        #         src_ip = item.get("Src IP",None)
        #         if src_ip not in unique_src_ips:
        #             unique_src_ips.append(src_ip)
        #             count += 1

        for item in data:  # 'data' là danh sách các từ điển (các record từ logs)
    # Kiểm tra nếu trường 'Label' tồn tại và bằng 1.0 (số thực)
            if float(item.get("Label", 0)) == 1.0:
                src_ip = item.get('Src IP', None)  # Lấy giá trị của Src IP
                dst_ip = item.get('Dst IP', None)  # Lấy giá trị của Dst IP
                
                if src_ip and src_ip not in unique_src_ips:
                    unique_src_ips.append(src_ip)
                    count += 1

                    # Tiêu đề email cảnh báo
                    # subject = "Thông báo cảnh báo từ hệ thống"

                    # # Tạo nội dung email với thông tin IP nguồn và đích
                    # body_template = (
                    #     "Chào bạn,\n\n"
                    #     "Hệ thống đã phát hiện hoạt động bất thường.\n"
                    #     "Đã phát hiện trinh sát từ IP nguồn: {src_ip} đến IP đích: {dst_ip}.\n\n"
                    #     "Vui lòng kiểm tra hệ thống để xác minh và xử lý kịp thời."
                    # )

                    # # Tạo nội dung email với thông tin chi tiết
                    # body = body_template.format(src_ip=src_ip, dst_ip=dst_ip)

                    # # Địa chỉ email đích
                    # to_email = "tiennam210152007@gmail.com"
                    
                    # # Gửi email
                    # if parseaddr(to_email)[1]:
                    #     success = send_email(subject, body, [to_email])
                    #     if success:
                    #         EmailNotification.objects.create(
                    #             email=to_email,
                    #             content=body,
                    #             timecreate=timezone.now()
                    #         )
                    #         print(f"Đã gửi email thành công và lưu lịch sử cho: {to_email}")
                    #     else:
                    #         print(f"Không thể gửi email tới: {to_email}")
                    # else:
                    #     print(f"Địa chỉ email không hợp lệ: {to_email}")


    return JsonResponse({'count': count, 'data': data}, safe=False)


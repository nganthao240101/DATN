from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import math,os
from cores.convert_json import csv_to_json
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
from cores.get_latest_file import get_latest_file
from cores.sendmail import send_email
import csv

def detect_view(request):
    return render(request,'detect/index.html')



from home.models import Prediction,UploadedFile,EmailFileRecord

def index(request):
    # Lấy tất cả các bản ghi từ mô hình Prediction
    data_list = Prediction.objects.all()
    print(data_list)
    
    # Truyền dữ liệu dưới dạng từ điển
    return render(request, 'detect/test.html', {'data_list': data_list})

def detect_core():
    # Lấy tất cả các đối tượng từ mô hình Prediction dưới dạng từ điển
    data_list = list(Prediction.objects.all().values())
    # print(data_list)

    # Xử lý dữ liệu
    for item in data_list:
        for key, value in item.items():
            if isinstance(value, (float, int)):  # Chỉ kiểm tra số
                if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
                    item[key] = None
                elif isinstance(value, int) and value < 0:
                    item[key] = 0
    return data_list

@csrf_exempt
def detect_filter(request):
    count = 0
    data=[]
    if request.method == 'POST' and 'pcap-file' in request.FILES:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploaded_file = request.FILES['pcap-file']
        save_path = os.path.join(base_dir, 'pcap_log', uploaded_file.name)
        print(request.FILES)

        
        # Lưu file PCAP vào đĩa
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Lưu thông tin file vào cơ sở dữ liệu
        file_info = UploadedFile(
            filename=uploaded_file.name,
            filesize=uploaded_file.size,
            filepath=save_path
        )
        file_info.save()
        
        data=detect_core()
        
        # Tính số lượng địa chỉ IP nguồn duy nhất có nhãn '1.0'
        unique_src_ips = []
        unique_dst_ips = []
        
        for item in data:
            if item.get("label") == '0.0':  # Sử dụng .get() để lấy giá trị
                src_ip = item.get('source_ip')
                dst_ip=item.get("destination_ip")
                  # Sử dụng .get() để tránh lỗi KeyError
                if src_ip and src_ip not in unique_src_ips:
                    unique_src_ips.append(src_ip)
                    count += 1

            # Kiểm tra và thêm IP đích vào danh sách nếu chưa tồn tại
                if dst_ip and dst_ip not in unique_dst_ips:
                    unique_dst_ips.append(dst_ip)
                body_content =f"Canh bao bat thuong tu dia chi {src_ip} den {dst_ip}\n"  # Thêm địa chỉ IP đích vào nội dung email
                subject = "Detected IP Addresses"
                to_emails = ["tranglucdinhkieu@gmail.com"]  # Danh sách email nhận
                send_email(subject, body_content, to_emails)
   

    return JsonResponse({'count': count, 'data': data}, safe=False)


@csrf_exempt
def logpcap_filter_time(request):
    data_dict = detect_core()

    # # Xử lý dữ liệu
    # for item in data_dict:
    #     for key, value in item.items():
    #         if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
    #             item[key] = None
    #         elif isinstance(value, int) and (value < 0):
    #             item[key] = 0
    # Xử lý lọc theo khoảng thời gian
    date_range = request.GET.get('daterange-with-time', None)
    if date_range:
        try:
            start_date_str, end_date_str = date_range.split(' - ')
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y %I:%M %p')
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y %I:%M %p')
        except ValueError:
            return JsonResponse({'error': 'Invalid date range format'}, status=400)

        filtered_data = [item for item in data_dict if start_date <= parser.parse(item['Timestamp']) <= end_date]
        return JsonResponse({'rows': filtered_data}, safe=False)

    first_100_items = data_dict[:1500]

    unique_src_ips = set()
    count = 0
    for item in data_dict:
        src_ip = item['Src IP']
        if src_ip not in unique_src_ips:
            unique_src_ips.add(src_ip)
            count += 1
    return JsonResponse({'total': count, 'rows': first_100_items}, safe=False)
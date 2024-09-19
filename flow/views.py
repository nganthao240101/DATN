import pandas as pd
import os
from django.shortcuts import render
import json

def read_flow_data_from_folder(folder_path):
    all_flows = []

    # Duyệt qua tất cả các tệp trong thư mục
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            
            # Đọc dữ liệu từ từng tệp CSV
            df = pd.read_csv(file_path)
            
            # Loại bỏ cột 'Dst Port' nếu có
            if 'Dst Port' in df.columns:
                df = df.drop(columns=['Dst Port'])
            
            # Xác định định dạng thời gian dự kiến
            try:
                # Thử chuyển đổi với định dạng thời gian cụ thể nếu bạn biết định dạng
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %I:%M:%S %p', errors='coerce')
            except ValueError:
                # Nếu không thành công, tự động xác định định dạng
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

            # Loại bỏ các giá trị NaT (thời gian không hợp lệ)
            df.dropna(subset=['Timestamp'], inplace=True)
            
            # Thêm dữ liệu vào danh sách
            all_flows.append(df)

    # Kiểm tra nếu không có dữ liệu hợp lệ
    if not all_flows:
        return {}  # Trả về một dictionary trống nếu không có dữ liệu hợp lệ

    # Kết hợp tất cả các DataFrame thành một
    combined_df = pd.concat(all_flows)

    # Nhóm dữ liệu theo thời gian (ví dụ: mỗi phút) và đếm số lượng luồng
    combined_df.set_index('Timestamp', inplace=True)
    flow_count = combined_df.resample('1T').size()  # Nhóm và đếm số lượng luồng theo mỗi phút

    # Chuyển kết quả thống kê sang dạng key-value với định dạng thời gian là chuỗi
    flow_statistics = flow_count.to_dict()
    flow_statistics = {str(k): v for k, v in flow_statistics.items()}  # Chuyển đổi Timestamp thành chuỗi

    return flow_statistics

def flow_chart_view(request):
    folder_path = '/home/ubuntu/Desktop/aipcap/TCPDUMP_and_CICFlowMeter/csv'
    flow_statistics = read_flow_data_from_folder(folder_path)
    print(flow_statistics)
    
    # Chuyển đổi dictionary keys (timestamps) và values (flow counts) sang list
    # Convert the labels and data to JSON strings
    labels_json = json.dumps(list(flow_statistics.keys()))
    data_json = json.dumps(list(flow_statistics.values()))

    context = {
        'labels_json': labels_json,
        'data_json': data_json,
    }
    
    return render(request, 'flow/index.html', context)

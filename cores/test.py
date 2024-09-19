import pandas as pd
import os

def read_flow_data_from_folder(folder_path):
    all_flows = []

    # Duyệt qua tất cả các tệp trong thư mục
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            
            # Đọc dữ liệu từ từng tệp CSV
            df = pd.read_csv(file_path)
            
            # Kiểm tra xem cột 'Dst Port' có tồn tại không và loại bỏ giá trị không cần thiết
            if 'Dst Port' in df.columns:
                values_to_remove = ['Dst Port']
                df = df[~df['Dst Port'].astype(str).isin(values_to_remove)]
            
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

    # Chuyển kết quả thống kê sang dạng key-value
    flow_statistics = flow_count.to_dict()

    return flow_statistics

# Đường dẫn đến thư mục chứa các tệp CSV của bạn
folder_path = '/home/ubuntu/Desktop/aipcap/TCPDUMP_and_CICFlowMeter/csv'

# Đọc và thống kê dữ liệu luồng từ tất cả các tệp CSV trong thư mục
flow_statistics = read_flow_data_from_folder(folder_path)

# In kết quả thống kê dưới dạng key-value
print("Kết quả thống kê:")
print(flow_statistics)

# In kiểu lưu trữ của kết quả thống kê
print("\nKiểu lưu trữ của kết quả thống kê:")
print(type(flow_statistics))

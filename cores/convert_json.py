import csv
from io import StringIO
from django.http import JsonResponse

def csv_to_json(data):
    if not data.strip():  # Kiểm tra nếu dữ liệu đầu vào trống
        return JsonResponse({"error": "Input data is empty"}, status=400)

    try:
        # Sử dụng StringIO để giả lập một file từ chuỗi CSV
        csv_file = StringIO(data)
        
        # Đọc nội dung chuỗi CSV như một file CSV
        csv_reader = csv.DictReader(csv_file)
        
        # Chuyển đổi dữ liệu từ CSV sang danh sách các dictionary
        data_json = []
        
        for row in csv_reader:
            # Xử lý mỗi dòng, ví dụ: chuyển đổi kiểu dữ liệu
            processed_row = {}
            for key, value in row.items():
                if value.isdigit():  # Kiểm tra nếu giá trị là số nguyên
                    processed_row[key] = int(value)
                else:
                    try:
                        processed_row[key] = float(value)  # Kiểm tra nếu giá trị có thể chuyển thành số thực
                    except ValueError:
                        processed_row[key] = value  # Giữ nguyên giá trị nếu không thể chuyển đổi
            
            data_json.append(processed_row)

        return data_json
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

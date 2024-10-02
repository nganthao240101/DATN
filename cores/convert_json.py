import csv
from io import StringIO
from django.http import JsonResponse

def csv_to_json(data):
    try:
        # Sử dụng StringIO để giả lập một file từ chuỗi CSV
        csv_file = StringIO(data)
        
        # Đọc nội dung chuỗi CSV như một file CSV
        csv_reader = csv.DictReader(csv_file)
        
        # Chuyển dữ liệu từ CSV sang danh sách các dictionary
        data_json = [row for row in csv_reader]
        return data_json
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
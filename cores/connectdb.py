import sqlite3

def execute_query(db_path, sql_query, params=None):
    try:
        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print(f"Đã kết nối thành công đến cơ sở dữ liệu: {db_path}")
        
        # Thực hiện câu lệnh SQL với các tham số nếu có
        if params:
            cursor.execute(sql_query, params)
            print("Them du lieu thanh cong")
        else:
            cursor.execute(sql_query)
            
        
        # Lưu thay đổi vào cơ sở dữ liệu nếu là lệnh cập nhật dữ liệu
        if sql_query.strip().upper().startswith("INSERT") or \
           sql_query.strip().upper().startswith("UPDATE") or \
           sql_query.strip().upper().startswith("DELETE"):
            connection.commit()
            print("Thay đổi đã được lưu thành công.")
        
        # Trả về dữ liệu cho các truy vấn SELECT
        if sql_query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            return result
        
    except sqlite3.Error as e:
        print(f"Đã xảy ra lỗi: {e}")
    
    finally:
        # Đóng kết nối
        if connection:
            connection.close()
            print("Kết nối cơ sở dữ liệu đã được đóng.")



# sql_insert = """
#     INSERT INTO home_realtimeprediction
#     (timestamp, source_ip, source_port, destination_ip, destination_port, 
#     flow_id, protocol, flow_duration,label)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """
    
#     # Lấy các giá trị từ DataFrame
# timestamp='5/9/2024  10:15:00 PM'
# source_ip='192.168.3.3'
# source_port=49240
# destination_ip='142.250.207.66'
# destination_port=443
# flow_id='192.168.3.3-142.250.207.66-49240-443-6'
# protocol='6'
# flow_dur=1462
# label='1'
# params_insert = (
#     timestamp,source_ip,source_port,destination_ip,destination_port,flow_id,protocol,flow_dur,label)

# execute_query('/home/ubuntu/Desktop/aipcap/db.sqlite3',sql_insert,params_insert)

# # Truy vấn để lấy tất cả dữ liệu từ bảng
# sql_select = """
#     SELECT * FROM home_realtimeprediction
# """

# # Thực thi truy vấn và lấy kết quả
# results = execute_query('/home/ubuntu/Desktop/aipcap/db.sqlite3', sql_select)

# # Hiển thị kết quả
# if results:
#     for row in results:
#         print(row)
# else:
#     print("Không có dữ liệu.")
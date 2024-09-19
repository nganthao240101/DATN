import psutil

def get_all_interfaces():
    """
    Lấy tất cả các giao diện mạng trên máy.
    
    :return: Danh sách tên các giao diện mạng.
    """
    interfaces = psutil.net_if_addrs()
    return list(interfaces.keys())

# Sử dụng hàm
all_interfaces = get_all_interfaces()
print("Tất cả các giao diện mạng:", all_interfaces)


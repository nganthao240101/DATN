import subprocess
import time
import signal
import psutil
import os

def get_all_interfaces():

    #Lấy tất cả các giao diện mạng trên máy.
    interfaces = psutil.net_if_addrs()
    return list(interfaces.keys())


def run_cicflowmeter(interface, output_dir, time_sleep):
 
    # Đảm bảo rằng thời gian chờ ít nhất là 5 giây
    assert time_sleep >= 5, "Thời gian chờ phải lớn hơn hoặc bằng 5 giây,Thời gian chạy trước khi dừng, tối thiểu 5 giây."
    
    # Lệnh để chạy script capture_interface_pcap.sh với tham số interface và output_dir
    command = ["/home/ubuntu/Desktop/aipcap/TCPDUMP_and_CICFlowMeter/capture_interface_pcap.sh", interface, output_dir]
    
    # Khởi chạy quá trình thực thi script
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(command, stdout=devnull, stderr=devnull)
    print("Quá trình capture_interface_pcap.sh đã bắt đầu.")
    
    # Chờ quá trình chạy trong thời gian quy định
    time.sleep(time_sleep)
    
    # Gửi tín hiệu SIGINT để dừng quá trình
    process.send_signal(signal.SIGINT)
    process.wait()  # Đợi quá trình kết thúc
    print("Quá trình capture_interface_pcap.sh đã được tắt.")

# Kiểm tra xem ens33 có phải là một giao diện hợp lệ không
all_interfaces = get_all_interfaces()

if 'ens33' in all_interfaces:
    # Giao diện ens33 tồn tại, chạy CICFlowMeter trên ens33
   
    output_directory = "/home/ubuntu/Desktop/aipcap/TCPDUMP_and_CICFlowMeter/pcap" 
    while True:
        run_cicflowmeter('ens33', output_directory, time_sleep=20)
        time.sleep(20)

else:
    print("Giao diện ens33 không tồn tại. Vui lòng kiểm tra lại.")

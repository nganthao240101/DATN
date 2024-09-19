
import subprocess
import time
import signal
# from cores.get_latest_file import get_latest_file
# from detect import read_csv_,predic_AE
# from get_latest_file import get_latest_file
# from detect import read_csv_,predict_AE
import os

def pcap_to_csv(input_pcap_file, output_dir):
    # Lệnh để chạy script convertpcaptocsv.sh với các tham số input_pcap_file và output_dir
    command = ['/home/ubuntu/Desktop/aipcap/TCPDUMP_and_CICFlowMeter/convert_csv.sh', input_pcap_file, output_dir]
    
    # Khởi chạy quá trình thực thi script và chuyển hướng stdout và stderr sang os.devnull
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(command, stdout=devnull, stderr=devnull)
          # Chờ cho quá trình hoàn tất
        process.communicate()

    # Khởi chạy quá trình thực thi script
    
    # process = subprocess.Popen(command)
    
  
    # Kiểm tra exit code để xác định quá trình có thành công hay không
    exit_code = process.returncode

    if exit_code == 0:
        return True
    else:
        return False
    
# while True:
#      # Sử dụng hàm
#     directory_path = "/home/ubuntu/Desktop/aipcap/pcap_log"
#     latest_file = get_latest_file(directory_path, "pcap")
#     print(f"File mới nhất: {latest_file}")
#     output_dir="/home/ubuntu/Desktop/aipcap/data_input"
# # # input_pcap_file=get_latest_file()
#     pcap_to_csv(latest_file,output_dir)
#     # dir_path = "/home/ubuntu/Desktop/aipcap/data_input"
#     # file = get_latest_file(output_dir, "csv")
#     # print("file",file)
#     # new_df=read_csv_(file)
#     # print("test",new_df.shape)
#     # predic_AE(new_df,file)
#     time.sleep(20)


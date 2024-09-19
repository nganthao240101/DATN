import re

def read_logpfsense(log_file_path):
    # Đọc dữ liệu từ tệp log
    def read_log_file(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()
    
    # Phân tích một dòng log
    def parse_log_line(line):
        pattern = r'(?P<timestamp>\S+) (?P<hostname>\S+) (?P<process>\S+)\[(?P<pid>\d+)\] (?P<unknown1>.*?),(?P<unknown2>.*?),(?P<id>\d+),(?P<interface>\S+),(?P<match>\S+),(?P<action>\S+),(?P<direction>\S+),(?P<protocol>\d+),(?P<ip_version>\S+),(?P<ip_header>\S+),(?P<flags>\S+),(?P<protocol_type>\S+),(?P<protocol_specific>\d+),(?P<src_ip>\S+),(?P<dst_ip>\S+),(?P<src_port>\d+),(?P<dst_port>\d+),(?P<byte_length>\d+)'
        match = re.match(pattern, line)
        if match:
            return match.groupdict()
        return None
    
    # Phân tích và xử lý dữ liệu log
    def parse_and_process_log(log_lines):
        logpfsense_list = []
        
        for line in log_lines:
            parsed_entry = parse_log_line(line)
            if parsed_entry:
                # Loại bỏ các trường có tên bắt đầu với 'unknown' hoặc dạng 'unknownX'
                cleaned_entry = {k: v for k, v in parsed_entry.items() if not re.match(r'^unknown\d*$', k, re.IGNORECASE)}
                
                logpfsense_list.append(cleaned_entry)
        
        return logpfsense_list
    
    log_lines = read_log_file(log_file_path)
    logpfsense_list = parse_and_process_log(log_lines)
    
    return logpfsense_list
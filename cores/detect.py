import pandas as pd
import pickle
import numpy as np
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torch.autograd import Variable
import sys
import os
import joblib
import time

# # Thêm thư mục cha vào sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import hàm get_file từ file get_latest_file.py
from get_latest_file import get_latest_file


columns = ['Destination Port', 'Flow Duration', 'Total Fwd Packets',
       'Total Backward Packets', 'Total Length of Fwd Packets',
       'Total Length of Bwd Packets', 'Fwd Packet Length Max',
       'Fwd Packet Length Min', 'Fwd Packet Length Mean',
       'Fwd Packet Length Std', 'Bwd Packet Length Max',
       'Bwd Packet Length Min', 'Bwd Packet Length Mean',
       'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s',
       'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
       'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max',
       'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std',
       'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
       'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
       'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
       'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
       'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
       'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
       'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
       'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
       'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
       'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
       'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
       'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean',
       'Idle Std', 'Idle Max', 'Idle Min']
# print(len(columns))
map_columns = {
    'Src IP': 'Src IP',
    'Src Port': 'Src Port',
    'Dst IP': 'Dst IP',
    'Dst Port': ' Destination Port',
    'Flow Duration': ' Flow Duration',
    'Total Fwd Packet': ' Total Fwd Packets',
    'Total Bwd packets': ' Total Backward Packets',
    'Total Length of Fwd Packet': 'Total Length of Fwd Packets',
    'Total Length of Bwd Packet': ' Total Length of Bwd Packets',
    'Fwd Packet Length Max': ' Fwd Packet Length Max',
    'Fwd Packet Length Min': ' Fwd Packet Length Min',
    'Fwd Packet Length Mean': ' Fwd Packet Length Mean',
    'Fwd Packet Length Std': ' Fwd Packet Length Std',
    'Bwd Packet Length Max': 'Bwd Packet Length Max',
    'Bwd Packet Length Min': ' Bwd Packet Length Min',
    'Bwd Packet Length Mean': ' Bwd Packet Length Mean',
    'Bwd Packet Length Std': ' Bwd Packet Length Std',
    'Flow Bytes/s': 'Flow Bytes/s',
    'Flow Packets/s': ' Flow Packets/s',
    'Flow IAT Mean': ' Flow IAT Mean',
    'Flow IAT Std': ' Flow IAT Std',
    'Flow IAT Max': ' Flow IAT Max',
    'Flow IAT Min': ' Flow IAT Min',
    'Fwd IAT Total': 'Fwd IAT Total',
    'Fwd IAT Mean': ' Fwd IAT Mean',
    'Fwd IAT Std': ' Fwd IAT Std',
    'Fwd IAT Max': ' Fwd IAT Max',
    'Fwd IAT Min': ' Fwd IAT Min',
    'Bwd IAT Total': 'Bwd IAT Total',
    'Bwd IAT Mean': ' Bwd IAT Mean',
    'Bwd IAT Std': ' Bwd IAT Std',
    'Bwd IAT Max': ' Bwd IAT Max',
    'Bwd IAT Min': ' Bwd IAT Min',
    'Fwd PSH Flags': 'Fwd PSH Flags',
    'Bwd PSH Flags': ' Bwd PSH Flags',
    'Fwd URG Flags': ' Fwd URG Flags',
    'Bwd URG Flags': ' Bwd URG Flags',
    'Fwd Header Length': ' Fwd Header Length',
    'Bwd Header Length': ' Bwd Header Length',
    'Fwd Packets/s': 'Fwd Packets/s',
    'Bwd Packets/s': ' Bwd Packets/s',
    'Packet Length Min': ' Min Packet Length',
    'Packet Length Max': ' Max Packet Length',
    'Packet Length Mean': ' Packet Length Mean',
    'Packet Length Std': ' Packet Length Std',
    'Packet Length Variance': ' Packet Length Variance',
    'FIN Flag Count': 'FIN Flag Count',
    'SYN Flag Count': ' SYN Flag Count',
    'RST Flag Count': ' RST Flag Count',
    'PSH Flag Count': ' PSH Flag Count',
    'ACK Flag Count': ' ACK Flag Count',
    'URG Flag Count': ' URG Flag Count',
    'CWR Flag Count': ' CWE Flag Count',
    'ECE Flag Count': ' ECE Flag Count',
    'Down/Up Ratio': ' Down/Up Ratio',
    'Average Packet Size': ' Average Packet Size',
    'Fwd Segment Size Avg': ' Avg Fwd Segment Size',
    'Bwd Segment Size Avg': ' Avg Bwd Segment Size',
    'Fwd Bytes/Bulk Avg': 'Fwd Avg Bytes/Bulk',
    'Fwd Packet/Bulk Avg': ' Fwd Avg Packets/Bulk',
    'Fwd Bulk Rate Avg': ' Fwd Avg Bulk Rate',
    'Bwd Bytes/Bulk Avg': ' Bwd Avg Bytes/Bulk',
    'Bwd Packet/Bulk Avg': ' Bwd Avg Packets/Bulk',
    'Bwd Bulk Rate Avg': 'Bwd Avg Bulk Rate',
    'Subflow Fwd Packets': 'Subflow Fwd Packets',
    'Subflow Fwd Bytes': ' Subflow Fwd Bytes',
    'Subflow Bwd Packets': ' Subflow Bwd Packets',
    'Subflow Bwd Bytes': ' Subflow Bwd Bytes',
    'FWD Init Win Bytes': 'Init_Win_bytes_forward',
    'Bwd Init Win Bytes': ' Init_Win_bytes_backward',
    'Fwd Act Data Pkts': ' act_data_pkt_fwd',
    'Fwd Seg Size Min': ' min_seg_size_forward',
    'Active Mean': 'Active Mean',
    'Active Std': ' Active Std',
    'Active Max': ' Active Max',
    'Active Min': ' Active Min',
    'Idle Mean': 'Idle Mean',
    'Idle Std': ' Idle Std',
    'Idle Max': ' Idle Max',
    'Idle Min': ' Idle Min',
}

# Define class Autoencoder 
class Encoder(nn.Module):
    
    def __init__(self, hidden_size):        
        super().__init__()
        
        self.fc1 = nn.Linear(input_size, hidden1_size)
        torch.nn.init.xavier_uniform_(self.fc1.weight)
        torch.nn.init.zeros_(self.fc1.bias)
    
        self.fc2 = nn.Linear(hidden1_size, hidden2_size)
        torch.nn.init.xavier_uniform_(self.fc2.weight)
        torch.nn.init.zeros_(self.fc2.bias)
    
        self.fc3 = nn.Linear(hidden2_size, hidden_size)
        torch.nn.init.xavier_uniform_(self.fc3.weight)
        torch.nn.init.zeros_(self.fc3.bias)
    
    def forward(self,x):
        out = x.view(x.size(0), input_size)
        out = torch.tanh(self.fc1(out))
        out = torch.tanh(self.fc2(out))
        out = self.fc3(out)
        return out
class Decoder (nn.Module):
    
    def __init__(self, hidden_size):        
        super().__init__()
        
        self.fc1 = nn.Linear(hidden_size, hidden2_size)
        self.fc1.weight.data = torch.Tensor(Encoder(hidden_size).fc3.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc1.bias)
                
        self.fc2 = nn.Linear(hidden2_size, hidden1_size)
        self.fc2.weight.data = torch.Tensor(Encoder(hidden_size).fc2.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc2.bias)
        
        self.fc3 = nn.Linear(hidden1_size, input_size)
        self.fc3.weight.data = torch.Tensor(Encoder(hidden_size).fc1.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc3.bias)
        
    def forward(self,x):
        out = torch.tanh(self.fc1(x))
        out = torch.tanh(self.fc2(out))
        out = torch.tanh(self.fc3(out))
        return out

hidden1_size = 39
hidden2_size = 19
hidden_size = 9
input_size = 77

# AE + classifier
d =hidden_size
encoder = Encoder(d)
decoder = Decoder(d)


import torch

with open("/home/ubuntu/Desktop/aipcap/cores/AE_28_8.pt", "rb") as f:
    encoder.load_state_dict(torch.load(f,weights_only=True))

import joblib
# Tải mô hình từ file
model = joblib.load('/home/ubuntu/Desktop/aipcap/cores/AE_DT_28_8.joblib')

# Tải mô hình từ file
scaler = joblib.load('/home/ubuntu/Desktop/aipcap/cores/saler_data.joblib')

# Sử dụng hàm

# print(f"File mới nhất: {latest_file}")


def read_csv_(file):
    df = pd.read_csv(file)
    # # Xác định header
    # header = df.columns.tolist()
    # # Xóa các hàng trùng với header
    # df_filtered = df[~df.apply(lambda row: row.tolist() == header, axis=1)]
    values_to_remove = ['Dst Port']
    df_filtered= df[~df['Dst Port'].isin(values_to_remove)]
    # Ghi đè DataFrame đã xử lý lên file CSV gốc
    df_filtered.to_csv(file, index=False)
    # Đọc lại file CSV đã xử lý vào DataFrame mới
    df_new = pd.read_csv(file)
    return df_new

def preprocessing(df):
    df.columns = df.columns.str.strip()
    df.rename(columns=map_columns, inplace=True)
    # df.columns = df.columns.str.strip()
    # print('Sau khi mapping',df.columns)
    # Remove rows where 'Dst Port' has specific values
    # values_to_remove = ['Dst Port']
    # df_= df[~df[' Destination Port'].isin(values_to_remove)]
    # Drop unnecessary columns
    df_copy = df.drop(columns=['Flow ID', 'Src IP', 'Dst IP', 'Src Port', 'Protocol', 'Timestamp', 'Label'])
    # df_copy[["Flow Bytes/s", " Flow Packets/s"]] = df_copy[["Flow Bytes/s", " Flow Packets/s"]].apply(pd.to_numeric,)
    new_cols = df_copy.columns
    new_df =  df_copy[new_cols]
    # print('Columns of df: ', df_copy.columns)
    # print('Shape of df: ', df_copy.shape)
    # print('Columns of new_df: ', new_df.shape)
    # print('Shape of new_df: ', new_df)
    new_df.drop_duplicates(inplace=True)
    new_df.replace('Infinity', -1, inplace=True)
    new_df.replace([np.inf, -np.inf, np.nan], -1, inplace=True)
    # print('Just New_df: ', new_df.shape)
    scaled = scaler.transform(new_df)
    return new_df,scaled


def predic_AE(df):
    new_df, scaled = preprocessing(df)
    realtime_tensor = torch.Tensor(scaled)
    encoded_realtime = encoder(realtime_tensor)
    encoded_realtime = encoded_realtime.detach().numpy()
    y_pred =model.predict(encoded_realtime)
    if len(y_pred) ==df.shape[0]:
        output = df.copy()
        output.columns = output.columns.str.strip()
        output['Timestamp'] = pd.to_datetime(output['Timestamp'], format='%d/%m/%Y %I:%M:%S %p')
        output['Label'] = y_pred
    else:
    # Nếu không khớp, bạn có thể cần phải điều chỉnh y_pred hoặc kiểm tra lỗi
        print(f'Length mismatch: DataFrame has {new_df.shape[0]} rows, but y_pred has {len(y_pred)} elements.')
    return output


from connectdb import execute_query
from datetime import datetime
db_path = '/home/ubuntu/Desktop/aipcap/db.sqlite3'
table_name = 'home_prediction'
while True:
    directory_path = "/home/ubuntu/Desktop/aipcap/data_input"
    latest_file = get_latest_file(directory_path, "csv")
    new_df=read_csv_(latest_file)
    output=predic_AE(new_df)
    print(output)

    output['Timestamp'] = output['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # time.sleep(20)
    # Đường dẫn đến cơ sở dữ liệu và tên bảng
    db_path="/home/ubuntu/Desktop/aipcap/db.sqlite3"
    # Vòng lặp để thêm dữ liệu vào cơ sở dữ liệu
    # Chuẩn bị câu lệnh SQL
    sql_insert = """
    INSERT INTO home_prediction 
    (timestamp, source_ip, source_port, destination_ip, destination_port, label)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    # Chuyển đổi các giá trị sang kiểu dữ liệu phù hợp
    for index, row in output.iterrows():
        params_insert = (
        row['Timestamp'],              # Thời gian dưới dạng chuỗi
        row['Src IP'],                # IP nguồn
        row['Src Port'],              # Cổng nguồn
        row['Dst IP'],                # IP đích
        row['Destination Port'],      # Cổng đích     # Thời gian luồng
        row['Label']                 # Nhãn
    )
        execute_query(db_path, sql_insert, params_insert)
    
        # Gọi hàm thực thi câu lệnh SQL với các tham số 
    time.sleep(20)



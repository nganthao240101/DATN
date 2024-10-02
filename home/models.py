from django.db import models
from django.utils import timezone

# Create your models here.

class Prediction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Thêm trường timestamp
    source_ip = models.CharField(max_length=15)  # Địa chỉ nguồn
    source_port = models.IntegerField()  # Cổng nguồn
    destination_ip = models.CharField(max_length=15)  # Địa chỉ đích
    destination_port = models.IntegerField()  # Cổng đích
    label = models.CharField(max_length=50)  # Nhãn dự đoán

    def __str__(self):
        return f"{self.timestamp} - {self.source_ip}:{self.source_port} -> {self.destination_ip}:{self.destination_port} - Label: {self.label}"
    
class UploadedFile(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    filesize = models.PositiveIntegerField()
    filepath = models.CharField(max_length=255)

    def __str__(self):
        return self.filename


class EmailFileRecord(models.Model):
    # Thời gian tạo
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Thông tin người dùng
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

class LogSnort(models.Model):
    time = models.DateTimeField()  # Thời gian sự kiện
    srcip = models.GenericIPAddressField()  # IP nguồn
    srcport = models.CharField(max_length=10)  # Cổng nguồn
    destip = models.GenericIPAddressField()  # IP đích
    destport = models.CharField(max_length=10)  # Cổng đích
    event = models.CharField(max_length=255)  # Sự kiện
    classification = models.CharField(max_length=255)  # Phân loại

    def __str__(self):
        return f"Event from {self.srcip} to {self.destip} on {self.time}"


class RealTimePrediction(models.Model):
    timestamp = models.DateTimeField()  # Trường thời gian
    source_ip = models.GenericIPAddressField()  # Trường địa chỉ IP nguồn
    source_port = models.IntegerField()  # Trường cổng nguồn
    destination_ip = models.GenericIPAddressField()  # Trường địa chỉ IP đích
    destination_port = models.IntegerField()  # Trường cổng đích
    flow_id = models.CharField(max_length=255)  # Trường ID luồng
    protocol = models.IntegerField()  # Trường giao thức
    flow_duration = models.IntegerField(unique=True)  # Trường thời gian luồng, đảm bảo giá trị duy nhất
    label = models.FloatField()  # Trường nhãn
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.source_ip}:{self.source_port} -> {self.destination_ip}:{self.destination_port} ({self.label})"


class LogPfSense(models.Model):
    timestamp = models.DateTimeField()  # Thời gian log
    action = models.CharField(max_length=255)  # Hành động
    protocol_type = models.CharField(max_length=50)  # Loại giao thức
    src_ip = models.GenericIPAddressField()  # IP nguồn
    dst_ip = models.GenericIPAddressField()  # IP đích
    src_port = models.CharField(max_length=10)  # Cổng nguồn
    dst_port = models.CharField(max_length=10)  # Cổng đích
    interface = models.CharField(max_length=50)  # Giao diện mạng (interface)

    def __str__(self):
        return f"{self.src_ip} -> {self.dst_ip} on {self.timestamp} via {self.interface}"
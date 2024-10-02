from django.shortcuts import render,redirect
import csv
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import EmailFileRecord
from datetime import datetime

def save_email(request):
    if request.method == "POST":
        name = request.POST.get('input-fullname')
        birthday_str = request.POST.get('input-birthday')
        email = request.POST.get('input-email')
        phone = request.POST.get('input-phone')

        try:
            # Chuyển đổi chuỗi ngày sinh thành dạng datetime
            birthday = datetime.strptime(birthday_str, '%d/%m/%Y').date()
            
            # Lưu thông tin vào database
            EmailFileRecord.objects.create(name=name, birthday=birthday, email=email, phone=phone)
                   
            messages.success(request, 'Thêm dữ liệu Email thành công!')
        except ValueError:
            messages.error(request, 'Ngày sinh không đúng định dạng (dd/mm/yyyy)!')
        except Exception as e:
            messages.error(request, f'Đã xảy ra lỗi: {str(e)}')

        return redirect('emailUser')

@login_required
def emailUser_view(request):
    dataEmail = EmailFileRecord.objects.all()
    context = {
        'data_email': dataEmail,
    }
    return render(request, 'email_user/index.html', context)


# def file_path_email():
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     file_path = os.path.join(base_dir, 'data', 'email_user.csv')
#     return file_path


# def add_contact_to_csv(file_path, name,dayofbirth, email, phone):
#     # Open the CSV file in append mode ('a')
#     with open(file_path, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
        
#         # Write the name, email, and phone to the CSV file
#         writer.writerow([name,dayofbirth, email, phone])
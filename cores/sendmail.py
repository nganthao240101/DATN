import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_emails):
    # Tạo đối tượng MIMEMultipart

    from_email = "ngan.nguyen.0168@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    login = "ngan.nguyen.0168@gmail.com"
    password = "iphf mrzm clvx skjv"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject

    # Thêm nội dung email vào đối tượng MIMEText
    msg.attach(MIMEText(body, 'plain'))

    # Thiết lập kết nối với máy chủ SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login, password)

        for to_email in to_emails:
            msg['To'] = to_email
            # Gửi email
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email đã được gửi thành công tới {to_email}!")
    except smtplib.SMTPException as e:
        print(f"Lỗi khi gửi email: {e}")
    finally:
        server.quit()

# Thông tin email và máy chủ SMTP
# subject = "Test Email"  # Tiêu đề
# body = "This is a test email sent from Python."  # Nội dung gửi
# to_emails = ["tranglucdinhkieu@gmail.com"]  # Danh sách email cần gửi


# # Gửi email
# send_email(subject, body, to_emails)

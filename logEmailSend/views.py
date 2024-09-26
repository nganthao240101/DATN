from django.shortcuts import render

from home.models import EmailNotification
def email_notification(request):
    data = EmailNotification.objects.all()
    context = {
        'data': data,
    }
    return render(request, 'logEmailSend/index.html', context)


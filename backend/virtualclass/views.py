from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

def signinuser(request):
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        pass

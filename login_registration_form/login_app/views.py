from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
import bcrypt

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }
    return render(request, 'index.html', context)

def process_user(request):
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    entered_password = request.POST['password']
    hash_pass = bcrypt.hashpw(entered_password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name= request.POST['first_name'],
        last_name= request.POST['last_name'],
        password = hash_pass,
        email = request.POST['email']
    )
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/success')

def success(request):
    context = {
        'logged_in_user': User.objects.get(id = request.session['user_id'])
    }
    return render(request,'success.html',context)

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return render (request,'index.html')
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')

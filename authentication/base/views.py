from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'base/index.html')



def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.info(request,'user is not exists ')
            return redirect('log_in')
            
        user = authenticate(username=username , password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        
        else:
            messages.info(request,'Username or password not match')
            return redirect('log_in')


    return render(request,'base/login.html')

# registration
def register(request):
    try:
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            com_password = request.POST['com_password']

            if password == com_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request,'user already exists')
                    return redirect('register')

                elif User.objects.filter(email=email).exists():
                    messages.error(request,'email already exists')
                    return redirect('register')

                else:
                    User.objects.create_user(first_name = fname,last_name = lname,username=username,email=email,password=com_password)  
                    messages.success(request,'Register successfully')   
                    return redirect('log_in')          
            else:
                messages.error(request,'password does not match')
                return redirect('register')
            
    except:
        messages.error(request,'All fields should be filled')
    

    return render(request,'base/register.html')


def log_out(request):
    logout(request)
    return redirect('log_in')


# change password while login 
@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            nm=form.save()
            update_session_auth_hash(request,nm) 
            return redirect('log_in')
    return render(request, "base/change_password.html", {'form':form}) 
    
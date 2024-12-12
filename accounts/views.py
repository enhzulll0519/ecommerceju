from django.shortcuts import redirect, render
from .models import Account
from .userForm import RegisterForm, AccountsForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required 

def user_register(request):
    if request.method == "POST":
        rform = RegisterForm(data=request.POST)
        aform = AccountsForm(data=request.POST)
        if rform.is_valid() and aform.is_valid():
            if rform['password'].value() == rform['repeat_password'].value():
                rform.instance.username = str(rform['email'].value()).split(sep="@")[0]
                user = rform.save()
                user.set_password(user.password)
                user.save()

                acc = aform.save(commit=False)
                acc.user = user
                if 'pro_image' in request.FILES:
                    acc.pro_image = request.FILES['pro_image']
                acc.save()
                messages.success(request, "registration is succesfull")
            else:
                messages.error(request, 'password not match')
        return redirect('register')
    else:
        r = RegisterForm()
        a = AccountsForm()
        context = {
            'aform': a,
            'rform':r,
        }
        return render(request, 'accounts/register.html', context)

def user_login(request):
    if request.method == 'POST':
        username = str(request.POST['username']).split(sep="@")[0]
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, "username password incorrect")
            return redirect('login')

    elif request.method == 'GET':
        return render(request, 'accounts/signin.html')

@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    return redirect('login')

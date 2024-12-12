from django.shortcuts import redirect, render
from .models import Account
from .userForm import RegisterForm, AccountsForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required 

from django.db import IntegrityError

def user_register(request):
    if request.method == "POST":
        rform = RegisterForm(data=request.POST)
        aform = AccountsForm(data=request.POST)
        if rform.is_valid() and aform.is_valid():
            if rform['password'].value() == rform['repeat_password'].value():
                # Generate the username based on email
                username = str(rform['email'].value()).split(sep="@")[0]
                
                # Ensure the username is unique
                user_exists = True
                counter = 1
                while user_exists:
                    try:
                        # Check if the user already exists with the generated username
                        user = rform.save(commit=False)
                        user.username = username
                        user.set_password(user.password)
                        user.save()
                        user_exists = False  # No error, stop the loop
                    except IntegrityError:
                        # Username conflict, so modify the username and try again
                        username = str(rform['email'].value()).split(sep="@")[0] + str(counter)
                        counter += 1
                
                # Save the additional account information
                acc = aform.save(commit=False)
                acc.user = user
                if 'pro_image' in request.FILES:
                    acc.pro_image = request.FILES['pro_image']
                acc.save()
                
                messages.success(request, "Registration successful")
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Invalid form data')
        return redirect('register')
    else:
        r = RegisterForm()
        a = AccountsForm()
        context = {
            'aform': a,
            'rform': r,
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

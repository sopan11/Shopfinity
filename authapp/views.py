from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def signup(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        try:
            if User.objects.get(username=email):
                messages.info(request, "User Already Exist")
                return render(request, 'authentication/signup.html')
        except Exception:
            pass

        if password!=confirm_password:
            messages.warning(request, "Password not matching")
            return render(request, 'authentication/signup.html')

        user = User.objects.create_user(email, email, password)
        user.save()
        return render(request, 'authentication/login.html')
    return render(request, 'authentication/signup.html')


def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        user_password = request.POST['pass1']

        myUser = authenticate(username=username, password=user_password)

        if myUser is not None:
            login(request, myUser)
            messages.info(request, "Login Success")
            return redirect('/')
        
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')
        
    return render(request, 'authentication/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/auth/login')

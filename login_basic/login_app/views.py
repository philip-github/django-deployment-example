from django.shortcuts import render
from login_app.forms import UserInfo,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.





def index(request):
    return render(request,'login_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("you are logged in , Nice!")



def regitser(request):

    registered = False

    if request.method == "POST":

        user_form = UserInfo(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            registered = True

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserInfo()
        profile_form = UserProfileInfoForm()

    return render(request,"login_app/registration_page.html",{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:

                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Username {} and password {} tried to login in and failed".format(username,password))
            return HttpResponse("invalid login details supplied!")

    return render(request,"login_app/login.html",{})

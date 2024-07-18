from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile


#Created a view for the main page
def index(request):
    return render(request, 'index.html')

#created view for signup page
def signup(request):

    #gets the user details from the signup form
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #checks if password,email and username are correct
        if password == password2:               
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page

                #create a profile object 
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')  
        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')

    #shows the signup page        
    else:
        return render(request,'signup.html')

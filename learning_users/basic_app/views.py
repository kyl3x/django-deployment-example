from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#this import is to manage logged in views etc. the view is defined below
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#make sure views don't override these imports

# Create your views here.

def index(request):
	return render(request, 'basic_app/index.html')

#to logout the user
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
#decorator needs to be directly above the logout request to be a requirement

@login_required
def logged_in(request):
    return HttpResponse ("You are logged in!")

def register(request): #This is to register a user by sending userinput to our DB

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


#Login Views

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        #get will retreive the username from the simple HTML form
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user: #this is in the DB
            if user.is_active:
                login(request,user) 
                #passing in the User info to login
                return HttpResponseRedirect(reverse('index')) 
                #redirects the user back to Homepage
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username {} and password {}".format(username,password)) 
            #don't do this in live but this shows error in console
            return HttpResponse("Invalid Login Details Supplied!")
    else:
        return render(request,'basic_app/login.html', {})



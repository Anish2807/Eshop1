from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

#==================================== User Signup ======================================================================

def signup(request):
	if request.method=='POST':
		fn=request.POST['fn']#firsh name
		ln=request.POST['ln']#last name
		un=request.POST['un']#username
		pw=request.POST['pw']#password
		eml=request.POST['eml']#email
		ph=request.POST['pn']#phone number
		ad=request.POST['ad']#address
		ty=request.POST['type']#user type
		user1=User(first_name=fn,last_name=ln,username=un,password=make_password(pw),email=eml)
		user1.save()#saving information into User table
		u=UserProfile(user=user1,usertype=ty,mobile=ph,address=ad)
		u.save()#saving information into UserProfile table
		return redirect('/signin/')
	return render(request,'signup.html')

#==================================== User Login ===================================================================

def signin_call(request):
	if request.method=="POST":
		un=request.POST['un']#user name
		pw=request.POST['pw']#password
		a=authenticate(username=un,password=pw)#authenticating user is valid or not
		if a:
			login(request,a)#creating login session
			#use=UserProfile.objects.get(user=a)
			use=UserProfile.objects.get(user__username=request.user)#retriving user object
			if use.usertype=='buyer':#if user is buyer it go into buyer model
				return redirect('/buyer/home/')
			elif use.usertype=='seller':#if user is buyer it go into seller model
				return redirect('/seller/home/')
			else:
				return HttpResponse('<h1>UserType None</h1>')#if user is not blongs from any type
		else:
			return HttpResponse('<h1>invalid username</h1>')#if user is not  valid is show 
	return render(request,'login.html')

#==================================== User LogOut============================================================================

def logout_call(request):
	logout(request)#logout request
	return redirect('/signin/')

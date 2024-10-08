from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.models import Cart,CartItem
from carts.views import _cart_id
# Create your views here.



def register(request):
  if request.method=='POST':
    form =RegistrationForm(request.POST)
    if form.is_valid():
      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      email=form.cleaned_data['email']
      username=form.cleaned_data['username']
      phone_no=form.cleaned_data['phone_no']
      password=form.cleaned_data['password']

      user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.phone_no=phone_no
      user.save()

      # user activation
      # current_site=get_current_site(request)
      # mail_subject="Please activate your account"
      # message=render_to_string('accounts/account_verification_email.html',{
      #   "user":user,
      #   "domain":current_site,
      #   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
      #   'token':default_token_generator.make_token(user)
      # })
      
      # to_email=email
      # send_email=EmailMessage(mail_subject,message,to=[to_email])
      # send_email.save()

      # messages.success(request,'Thank yoy for registering with us. We have sent to you and email verification email to your email address. Please verify it.')

      return redirect('/accounts/login/?command=verification&email='+email)

  else:
    form=RegistrationForm()
  context={
    'form':form
  }
  return render(request,'accounts/register.html',context)



def activate(request,uidb64,token):
  try:
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account._default_manager.get(pk=uid)
  except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
    user=None

  if user is not None and default_token_generator.check_token(user,token):
    user.is_active=True
    user.save()
    messages.success(request,"Congratulations! Your accunt is activated")
    return redirect('login')
  else:
    messages.error(request,"Invalid activation link")
    return redirect('register')


def login(request):
  if request.method=='POST':
    email=request.POST['email']
    password=request.POST['password']

    user=auth.authenticate(email=email,password=password)
    
    if user is not None:
      try:
         cart =Cart.objects.get(cart_id=_cart_id(request))
         is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()

         if is_cart_item_exists:
           cart_item=CartItem.objects.filter(cart=cart)

           for item in cart_item:
             item.user=user
             item.save()
             
      except:
        pass

      auth.login(request,user)
      messages.success(request,"You are now logged in")
      return redirect('dashboard')
    else:
      messages.error(request,"Invalid login credentials")
      return redirect('login')
  else:
    return render(request,'accounts/login.html')


@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  messages.success(request,'You are logged out')
  return redirect('login')



@login_required(login_url='login')
def dashboard(request):
  return render(request,'accounts/dashboard.html')


def forgetPassword(request):
  if request.method=='POST':
    email=request.POST['email']
    if Account.objects.filter(email=email).exists():
      user=Account.objects.get(email__exact=email)

      # current_site=get_current_site(request)
      # mail_subject="Reset your password"
      # message=render_to_string('accounts/reset_password_email.html',{
      #   "user":user,
      #   "domain":current_site,
      #   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
      #   'token':default_token_generator.make_token(user)
      # })
      
      # to_email=email
      # send_email=EmailMessage(mail_subject,message,to=[to_email])
      # send_email.save()

      messages.success(request,'Password reset email has been send to your email address')
      return redirect('login')
    else:
      messages.error(request,"Account does not exists")
      return redirect('forgetPassword')

  
  return render(request,'accounts/forgetPassword.html')


def reset_password_validate(request,uidb64,token):
  try:
      uid=urlsafe_base64_decode(uidb64).decode()
      user=Account._default_manager.get(pk=uid)
  except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
      user=None
 
  if user is not None and default_token_generator.check_token(user,token):
      request.session['uid']=uid
      messages.success(request,"Please reset your password")
      return redirect('resetPassword')
  else:
     messages.error(request,"This link has been expaired")
  return redirect('login')


def resetPassword(request):
  if request.method=='POST':
    pasword=request.POST['password']
    confirm_password=request.POST['confirm_password']

    if pasword==confirm_password:
      uid=request.session.get['uid']
      user=Account.objects.get(pk=uid)
      user.set_password(pasword)
      user.save()
      messages.success(request,'Password reset success')
      return redirect('login')
    else:
      messages.error(request,"Password do not match")
      return redirect('resetPassword')
  else:  
    return render(request,'accounts/resetPassword.html')
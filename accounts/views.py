import email
import ast
from itertools import product
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from accounts.forms import RegistrationForm, UserAuthenticationForm, ProfileEdit, UserChangeForm
from .models import Product, Cart


import email
# from sms import send_sms
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from accounts.models import CustomUser, UserFiles
from .helpers import send_otp_email
from accounts.forms import RegistrationForm, UserAuthenticationForm, ProfileEdit, OTPVerificationForm, OrganizationAndHealthcareProfessionalSearchForm, FileUploadForm

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            #login(request,user)
            #return render(request, 'registration/otp.html',context)
            request.session['username'] = username
            request.session['password'] = raw_password
            #send_otp_email(user)
            return redirect('otp_email')
            #return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html',context)

# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
            if user.user_type=='patient':
                    return redirect("patient_index") 
            elif user.user_type=='hospital':
                    return redirect("hospital_index")
            elif user.user_type=='pharmacy':
                    return redirect("pharmacy_index")
            elif user.user_type=='insurance':
                    return redirect("insurance_index")
            else:
                    return redirect("health_prof_index")
        
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            #user should not be able to login till email is verified
            if not user.is_email_verified:
                request.session['username'] = username
                request.session['password'] = password
                #send_otp_email(user)
                return redirect("otp_email")

           
            if user.user_type=='patient':
                    #send_otp_email(user)
                    login(request,user)
                    return redirect("patient_index") 
            elif user.user_type=='hospital':
                    login(request,user)
                    return redirect("hospital_index")
            elif user.user_type=='pharmacy':
                    login(request,user)
                    return redirect("pharmacy_index")
            elif user.user_type=='insurance':
                    login(request,user)
                    return redirect("insurance_index")
            else:
                    login(request,user)
                    return redirect("health_prof_index")
            
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request,'registration/login.html',context)

@login_required(login_url='/login/')
def editprofile(request):
    context = {}
    
    user=request.user
    if not user.is_authenticated:
        return redirect('login')
    
    if request.POST:
        form=ProfileEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        
    else:
        form = ProfileEdit(initial={"email":request.user.email, "username":request.user.username,
                                    "official_name":request.user.official_name,"mobile":request.user.mobile,
                                    "user_type":request.user.user_type,
                                    "address":request.user.address})
    

    context['edit_form']= form
    return render(request, 'registration/edit.html',context)
    
    def get_object(self):
        return self.request.user

@login_required(login_url='/login/')
def patient_view(request):
    context = {}
    user=request.user
    if user.user_type != 'patient':
        return redirect('login')
    if request.POST:
        form = OrganizationAndHealthcareProfessionalSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('user_type') == 'all':
                users = CustomUser.objects.filter(official_name__contains=form.cleaned_data.get('name')).exclude(user_type="patient")
            else:
                users = CustomUser.objects.filter(official_name__contains=form.cleaned_data.get('name'),user_type = form.cleaned_data.get('user_type')).exclude(user_type="patient")
    else:
        form = OrganizationAndHealthcareProfessionalSearchForm(initial={'user_type':'all'})
        users = CustomUser.objects.exclude(user_type="patient")
        
    context['org_healthcare_profs'] = users
    context['search_form'] = form   
    return render(request, 'patient_index.html',context) 

@login_required(login_url='/login/')
def hospital_view(request):
    if request.user.user_type != 'hospital':
        return redirect('login')
    return render(request, 'hospital_index.html') 

@login_required(login_url='/login/')
def insurance_view(request):
    if request.user.user_type != 'insurance':
        return redirect('login')
    return render(request, 'ins_index.html')

@login_required(login_url='/login/')
def pharmacy_view(request):
    if request.user.user_type != 'pharmacy':
        return redirect('login')
    return render(request, 'pharmacy_index.html')

@login_required(login_url='/login/')
def healthcare_prof_view(request):
    if request.user.user_type != 'professional':
        return redirect('login')
    return render(request, 'health_index.html')



def otp_email_view(request):
    context = {}
    user=request.user

    # if not user.is_authenticated: 
    #      return redirect('login')

    user = authenticate(username=request.session.get('username'),password=request.session.get('password'))
    if not user:
        return redirect('login')
    if request.POST:
        form = OTPVerificationForm(request.POST, request=request)
        if form.is_valid():
            #form.save()
            user.is_email_verified = True
            user.save()
            return redirect('login')
        
    else:
        form = OTPVerificationForm(request=request)
        send_otp_email(user)

    context['otp_form'] = form   
    return render(request,'registration/otp.html',context)

     
@login_required(login_url='/login/')
def show_files_view(request):
    context={}
    files = UserFiles.objects.filter(user=request.user)
    context['files'] = files
    return render(request,"show_files.html",context)

def delete_file_view(request,pk):
    if request.POST:
        file = UserFiles.objects.get(pk=pk)
        file.delete()
    return redirect('show_file')

@login_required(login_url='/login/')
def upload_file_view(request):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    if request.POST:
        form = FileUploadForm(request.POST,request.FILES,request=request)#, instance=request.user,request=request)
        if form.is_valid():
            print(request.user.official_name)
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('show_file')
    else:
        form = FileUploadForm(request=request)#instance=request.user,request=request)
    context['file_form'] = form
    return render(request,"upload_file.html",context) 

def cart(request):
    productsss = Product.objects.all()
    #  print(productsss.values)
    #  print(request.POST)

    if request.POST:
        res = request.POST
        products_dict = {}
        for i in productsss:
            products_dict[i.id] = {'quantity':res[i.name], 'cost_per_medicine':i.price}
        print(products_dict)
        amount = add_to_cart(products_dict)
    else:
        return render(request, 'patient_index.html',{'products':productsss})

    return redirect(f'/payments/views/homepage?amount={amount}', amount=amount)
    
    # return render(request, 'payments_template/payment_success.html', {'amount':amount})
    
    

def add_to_cart(cart_dict):
    amount=0
    for k,v in cart_dict.items():
        # item = Cart(product=k, quantity=v)
        amount+=ast.literal_eval(v['quantity'])*v['cost_per_medicine']
        print(amount)
        item = Cart(product=k, quantity=v['quantity'], amount=amount)
        item.save()
    return amount







   
    



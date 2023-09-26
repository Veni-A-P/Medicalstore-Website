from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine
from .forms import MedicineForm
from datetime  import date

#Signup page    
def Signup(request):
    if request.method == 'POST':
        username =request.POST.get('username')
        email =request.POST.get('email') 
        password =request.POST.get('password')
        confirm_password =request.POST.get('confirm_password')
        
        if not username or not email or not password  or not confirm_password:
            messages.error(request, 'Please provide username, email, password, and confirm password')
            
        elif User.objects.filter(username=username).exists():
            messages.error(request,'Username already taken') 
              
        elif User.objects.filter(email=email).exists():   
            messages.error(request,'Email already taken')
            
        elif password!= confirm_password:
            messages.error(request,'Your password and confirm password are not Same!!')  
                  
        else:
            my_user=User.objects.create_user(username,email,password)
            my_user.save()
            messages.success(request,"successsfully created")
            return redirect('login')
        
    return render(request,'signup.html')    

#Login page
def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('add')
        else:
            messages.error(request,"Invalid password!")
    return render(request,'login.html') 

#Logout Page
def Logout(request):
    logout(request)
    return redirect('login')

# Index Page
@login_required

def Add(request):
    
    form = MedicineForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('list') 
    context ={
        'form':form,
       
    } 
    return render(request,'add.html',context)

#List function 
@login_required
def List(request):
    medicine = Medicine.objects.all()
    today = date.today()     
    context = {
        'medicine': medicine,
        'today':today
        } 
    
    return render(request,'list.html',context)

#Update function
@login_required
def Update(request,id):
    medicine = Medicine.objects.get(id = id)
    if request.method == "POST":
        form = MedicineForm(request.POST,instance=medicine)
        if form.is_valid():
            form.save()
        return redirect('list') 
    else:
        form = MedicineForm(instance = medicine)  
    context= {
        'form': form,
        'medicine':medicine
        }
    return render (request,'update.html',context)

#Delete function
@login_required
def Delete(request,id):
    medicine = Medicine.objects.get(id = id)
    if request.method == "POST":
        medicine.delete()
        return redirect('list')
    context = {
        "medicine":medicine,
        }
    return  render(request,'delete.html',context)

#search
@login_required
def Search(request):
    query =request.GET['query']
    medicine= Medicine.objects.filter(Name__istartswith = query)
    context ={
        'medicine':medicine
        }
    return render(request,'search.html',context) 

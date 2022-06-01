from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import  RegisterUserForm
def register (request):
    if request.method!='POST':
        form=RegisterUserForm()
    else:
        form=RegisterUserForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            return redirect( 'home')
    context={'form':form}
    return render(request,'registration/register.html',context)
# Create your views here.

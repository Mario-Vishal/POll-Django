from django.shortcuts import render, HttpResponse, redirect, get_object_or_404,HttpResponseRedirect
from .models import Options, Poll, PollVoted
from django.forms import inlineformset_factory

#auth
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#custom forms
from .forms import PollForm,OptionsForm, SignUpForm,OptionsFormset

import re

# Create your views here.
def home(request):
    
    polls = Poll.objects.all().order_by('-poll_date')

    if request.user.is_authenticated:
        return render(request,"poll/home.html",{'polls':polls})

    return render(request,"poll/home.html",{'polls':polls,'pollvoted':''})



def signupuser(request):
    
    error=""
    if request.method == "GET":

        return render(request,'poll/signup.html',{'form':SignUpForm(),'error':error})
    else:
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError as e:
            error="Not a Valid email"

            return render(request,'poll/signup.html',{'form':SignUpForm(),'error':error})

        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    email = request.POST["email"]
                )

                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                error="Username already taken! try another."
                return render(request,'poll/signup.html',{'form':SignUpForm(),'error':error})


        else:
            error="Passwords do not match"
            return render(request,'poll/signup.html',{'form':SignUpForm(),'error':error})



def loginuser(request):
    if request.method == "GET":
        return render(request,'poll/loginuser.html',{'form':AuthenticationForm()})
    else:
        uname = request.POST['username']
        passkey = request.POST['password']
        user = authenticate(request,username = uname,password = passkey)
        if user is None:
            return render(request,'todo/login.html',{'form':AuthenticationForm(),'error':"user credentials are wrong!"})

        else:
            login(request,user)
            return redirect('home')

def logoutuser(request):
    
    logout(request)
    return redirect('home')


def polldetail(request,poll_pk):

    if not request.user.is_authenticated:
        return redirect('signupuser')

    
    if request.method == "POST":

        display=False

        poll = Poll.objects.get(pk=poll_pk)

        if hasVoted(poll_pk,request.user):
            options = Options.objects.filter(poll_id=poll_pk)
            display=True
            total = calTotal(options)
            
            return render(request,"poll/polldetail.html",{'poll':poll,'options':options,'display':display,'total':total})
        
        selected_option =  request.POST.get('vote-option')
        if selected_option:
            # option = Options.objects.get(poll_id=poll_pk,pk=selected_option)
            option = get_object_or_404(Options,pk=selected_option,poll_id=poll_pk)
            
            option.votes = option.votes + 1
            option.save()
            pollvoted = PollVoted()
            pollvoted.poll_id = poll
            pollvoted.user = request.user
            pollvoted.voted = True
            pollvoted.save()

            print(option.votes,option.name)

            display=True
        options = Options.objects.filter(poll_id=poll_pk)
        total=calTotal(options)

        return render(request,"poll/polldetail.html",{'poll':poll,'options':options,'display':display,'total':total})

    else:
        display=False
        poll = Poll.objects.get(pk=poll_pk)
        options = Options.objects.filter(poll_id=poll_pk)
        total=calTotal(options)
        return render(request,"poll/polldetail.html",{'poll':poll,'options':options,'display':display,'total':total})

def calTotal(options):
    total=0
    for opt in options:
            total+=opt.votes

    return total



def hasVoted(pk,user):

    try:
        poll = Poll.objects.get(pk=pk)
        pollvoted = get_object_or_404(PollVoted,poll_id =poll ,user = user)
        print(pollvoted.voted)
    except:
        return False
    
    return pollvoted.voted


def createpoll(request):
   
 
    if request.method=="GET":
        formset = OptionsFormset(request.GET or None)
    
    if request.method=="POST":

        
        formset = OptionsFormset(request.POST)
        if not len(formset)>=2:
            error="should have atleast 2 options"
            
            return render(request,"poll/createpoll.html",{'form':PollForm(),'formset':formset,'error':error})

        poll = Poll.objects.create(user=request.user)
        if formset.is_valid():
            q = request.POST.get('poll_question')
            poll.poll_question = q
            poll.option_number = len(formset)
            poll.save()
            
            for form in formset:
            
                name = form.cleaned_data.get('name');
                op = Options(poll_id=poll,name=name)
                op.save()
            
            return redirect('polldetail',poll.id)
        
    return render(request,"poll/createpoll.html",{'form':PollForm(),'formset':formset})


def ifFormPost(forms):

    if forms.is_valid():

        for form in forms:

            value = form.cleaned_data.get('form-1-data')
            if value=="0":
                return False

            else:
                return True

    else:
        return False





def yourpolls(request):

    user_polls = Poll.objects.filter(user = request.user).all()
    
    return render(request,'poll/yourpolls.html',{'polls':user_polls})


def deletepoll(request,poll_pk):

    poll = get_object_or_404(Poll,pk=poll_pk,user = request.user)
    poll.delete()
    
    return redirect('yourpolls')


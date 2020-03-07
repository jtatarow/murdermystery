from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TransferForm
from .forms import UserEditForm, KillerForm
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Auth seccuessful")
                else:
                    return HttpResponse("Disabled")
            else:
                return HttpResponse("Invalid")
    else:
        form = LoginForm()
        
    return render(request, 'bank/login.html', {'form': form})


@login_required
def dashboard(request):
    user = Profile.objects.get(user=request.user.id)
    balance = user.balance
    alive = "alive" if user.alive else "dead"
    return render(request, 'bank/dashboard.html',
                  {'section': 'dashboard', 'balance': balance, 'alive': alive})
    

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user, balance=1000)
            return render(request,
                          'bank/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    
    return render(request,
                  'bank/register.html',
                  {'user_form': user_form})

@login_required
def transfer(request):
    if request.method == 'POST':
        transfer_form = TransferForm()
        amount = abs(float(request.POST['amount']))
        if not request.user.profile.alive:
            messages.error(request, "You can't transfer money, you're dead!")
        elif amount <= request.user.profile.balance and request.user.profile.alive:
            target_user = Profile.objects.filter(user__pk=request.POST['Player'])[0]
            target_user.balance += amount
            request.user.profile.balance -= amount
            
            target_user.save()
            request.user.profile.save()
            
            messages.success(request, 'Transfer complete')
        else:
            messages.error(request, "You do not have enough to transfer")
    else:
        transfer_form = TransferForm()
    
    return render(request,
                  'bank/transfer.html',
                  {'transfer_form': transfer_form})

@login_required
def edit(request):
    if request.method == 'POST':
        print(request.FILES["image"])
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'bank/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def killer(request):
    if not request.user.profile.killer:
        messages.error(request, 'You are not the killer')
        return redirect('dashboard')

    if request.method == 'POST':
        killer_form = KillerForm()
        target_user = Profile.objects.get(user__pk=request.POST['Player'])

        if not target_user.alive:
            messages.error(request, "They are already dead!")
        elif target_user.user == request.user:
            messages.error(request, "You can't kill yourself, you still have work to do")
        else:
            target_user.alive = False
        
            target_user.save()
            
            messages.success(request, 'Murder complete')
            return redirect('dashboard')


    else:
        killer_form = KillerForm()

    return render(request, 'bank/killer.html', {'killer_form': killer_form})

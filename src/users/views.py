from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f"You are logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, f'Unable to login Try Again')
        else:
            messages.error(request, f'Login Failed Please Try Again')
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'login_form': login_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


class RegisterView(View):

    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(
                request, f'User {user.username} registered successfully.')
            return redirect('home')
        else:
            messages.error(request, f'An error occured trying to register.')
            return render(request, 'views/register.html', {'register_form': register_form})
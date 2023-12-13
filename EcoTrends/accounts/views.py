from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash   
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from django.template import loader
from django.http import HttpResponse
from .forms import CustomUserChangeForm,CustomPasswordChangeForm
from catalog.models import Comment, SavedProduct, Product

# Create your views here.

def register_view(request):#view for signing up
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):#View for the log in 
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('')#I forgot to fill this and it worked anyway. I am not sure why 
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):#view to log out of one's account
    logout(request)
    return redirect('/')
def delete_account(request):#method to delete one's account. 
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted.')
        return redirect('catalog:product_list')  
    return render(request, 'accounts/delete_account.html')
@login_required
def profile_view(request):#view that returns the profile template. Only accessible for users that are logged in. They can change their credentials and view their comments and saved products in that template
    user = request.user
    comments = Comment.objects.filter(user=user)
    user_saved_products = SavedProduct.objects.filter(user=user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    return render(request, 'accounts/profile.html', {'user': user, 'user_form': user_form, 'password_form': password_form, 'comments': comments, 'user_saved_products': user_saved_products})
class CustomLoginView(LoginView):#view fpr the login template. After a succesfull login, the user is redirected to their profile
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile') 

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)  
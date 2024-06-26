from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from register.forms import UpdateForm
from django.contrib.auth import logout as lt
from django.contrib import messages
from django.contrib.auth.models import User

#usernames = [user.username for user in User.objects.all()]

def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("update_profile")
    context.update({
        "form":form, 
        "title": "Rejestracja",
    })
    return render(request, "register/signup.html", context)

def signin(request):
    context = {}
    form = AuthenticationForm(request, data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    context.update({
        "form": form,
        "title": "Logowanie",
    })
    return render(request, "register/signin.html", context)

@login_required
def update_profile(request):
    context = {}
    user = request.user
    form = UpdateForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')
            if not fullname or not bio or not profile_pic:
                messages.error(request,
                               "Wszystkie pola (Imię i nazwisko, Biogram, Zdjęcie profilowe) muszą być uzupełnione.")
            else:
                update_profile = form.save(commit=False)
                update_profile.user = user
                update_profile.save()
                return redirect("home")
        else:
            return redirect("update_profile")
    context.update({
        "form": form,
        "title": "Aktualizacja profilu",
    })

    return render(request, "register/update.html", context)

@login_required
def logout(request):
    lt(request)
    return redirect("home")
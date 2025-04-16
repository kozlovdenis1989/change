from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Главная, вещи
def home(request):
    content = None
    return render(request, 'index.html', content)
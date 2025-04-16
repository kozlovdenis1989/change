from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Item, ExchangeProposal

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

# Главная
def home(request):
    items_list = Item.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if category:
        items_list = items_list.filter(category=category)
    if condition:
        items_list = items_list.filter(condition=condition)

    paginator = Paginator(items_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передаем выбранные значения и списки для селектов
    categories = Item.CATEGORY_CHOICES
    conditions = Item.CONDITIONS

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'conditions': conditions,
        'selected_category': category,
        'selected_condition': condition,
    }
    return render(request, 'index.html', context)

# Детали
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'detail.html', {'item': item})
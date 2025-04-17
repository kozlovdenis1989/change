from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Item, ExchangeProposal
from .forms import ItemForm

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
    
    category = request.GET.get('category', "")
    condition = request.GET.get('condition', "")
    query = request.GET.get('search', "")

    filter_params = {}

    if category:
        filter_params['category'] = category
    if condition:
        filter_params['condition'] = condition

    items_list = Item.objects.filter(**filter_params).order_by('-created_at')

    if query:
        items_list = items_list.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(items_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Передаем выбранные значения и списки для селектов
    categories = Item.CATEGORY_CHOICES
    conditions = Item.CONDITIONS

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'conditions': conditions,
        'selected_category': category,
        'selected_condition': condition,
        'search': query
    }
    return render(request, 'index.html', context)

# Детали
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'detail.html', {'item': item})


@login_required  
def my_items(request):
    user_items = Item.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'items': user_items,
    }
    return render(request, 'my_items.html', context)



@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)  # чтобы редактировал только владелец
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'create_or_edit_item.html', {'form': form})

@login_required
def create_item(request):
    # чтобы редактировал только владелец
    if request.method == 'POST':
        form = ItemForm()
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm()
    return render(request, 'create_or_edit_item.html', {'form': form})
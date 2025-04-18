from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Item, ExchangeProposal
from .forms import ItemForm, ExchangeProposalForm
from django.http import HttpResponseForbidden

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

    if request.user.is_authenticated:
        items_list = items_list.filter(~Q(user=request.user.id) )

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
    item_sender = ExchangeProposal.objects.values_list("item_sender", flat=True)
    print(item_sender)
    context = {
        'items': user_items,
        'item_sender': item_sender
    }
    return render(request, 'my_items.html', context)



@login_required
def edit_item(request, pk):
    title = 'Редактирование объявления'
    item = get_object_or_404(Item, pk=pk, user=request.user)  
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'create_or_edit_item.html', {'form': form, 'title': title})

@login_required
def create_item(request):
    if request.method == 'POST':
        
        form = ItemForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            item = form.save(commit=False)  
            item.user = request.user 
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm()
    return render(request, 'create_or_edit_item.html', {'form': form, 'title': 'Создать объявление'})

@login_required
def delete_item(request, pk):
    
    item= get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('my_items')  
    return render(request, 'delete.html', {'item': item})

@login_required
def delete_proposal(request, pk):
    
    proposal = get_object_or_404(ExchangeProposal, item_sender=pk)
    if request.method == 'POST':
        proposal.delete()
        return redirect('my_items')  
    return render(request, 'delete.html', {'item': proposal})
    

@login_required
def create_proposal(request, pk_other, pk_my=None):
    other_item = get_object_or_404(Item, pk=pk_other)

    if pk_my is None:
        used_item_ids = ExchangeProposal.objects.filter(item_sender__user=request.user).values_list('item_sender_id', flat=True)
        user_items = Item.objects.filter(user=request.user).exclude(id__in=used_item_ids).order_by('-created_at')

        context = {
            'items': user_items,
            'pk_other': pk_other,
        }
        return render(request, 'create_proposal.html', context)
    

    my_item = get_object_or_404(Item, pk=pk_my, user=request.user)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, item_sender=my_item, item_receiver=other_item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ExchangeProposalForm(item_sender=my_item, item_receiver=other_item)

    return render(request, 'create_or_edit_item.html', {'form': form, 'title': 'Комментарий к обмену'})


@login_required
def exchange_proposals(request):
    proposals = ExchangeProposal.objects.all()

    sort_by = request.GET.get('sort', 'date')  # по умолчанию сортируем по дате

    my_proposals = request.GET.get('my_proposals', '')
    if my_proposals:
        proposals = proposals.filter(
            Q(item_sender__user=request.user) | Q(item_receiver__user=request.user)
        )



    if sort_by == 'author':
        # Сортируем по отправителю (username)
        proposals = proposals.order_by('item_sender')
    elif sort_by == 'status':
        # Сортируем по статусу, а потом по дате
        proposals = proposals.order_by('status')
    
    else:
        # По дате, по убыванию (последние сверху)
        proposals = proposals.order_by('-created_at')

    
    if request.method == 'POST':
        proposal_id = request.POST.get('proposal_id')
        new_status = request.POST.get('status')
        if proposal_id and new_status in dict(ExchangeProposal.STATUS_CHOICES).keys():
            try:
                proposal = ExchangeProposal.objects.get(pk=proposal_id)
            except ExchangeProposal.DoesNotExist:
                proposal = None

           
            if proposal and proposal.item_receiver.user == request.user:
                proposal.status = new_status
                proposal.save()
            else:
                return HttpResponseForbidden("Нельзя изменить статус этого предложения.")

        
        from django.shortcuts import redirect
        return redirect('exchange_proposals')

    context = {
        'proposals': proposals,
        'title': 'Список предложений обмена',
        'sort_by': sort_by,
    }
    return render(request, 'exchange_proposals.html', context)
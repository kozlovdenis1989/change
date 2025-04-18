import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Item, ExchangeProposal

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', password='pass')
    assert user.username == 'testuser'
    assert user.check_password('pass')

@pytest.mark.django_db
def test_item_creation():
    user = User.objects.create_user(username='owner')
    item = Item.objects.create(
        user=user,
        title='Test Item',
        description='Description',
        category='мебель',
        condition='new'
    )
    assert str(item) == 'Test Item'
    assert item.user == user

@pytest.mark.django_db
def test_exchangeproposal_creation():
    user1 = User.objects.create_user(username='user1')
    user2 = User.objects.create_user(username='user2')

    item1 = Item.objects.create(user=user1, title='Item 1', description='Desc', category='книги', condition='used')
    item2 = Item.objects.create(user=user2, title='Item 2', description='Desc', category='мебель', condition='new')

    proposal = ExchangeProposal.objects.create(
        item_sender=item1,
        item_receiver=item2,
        comment='Let\'s trade',
        status='pending'
    )
    assert str(proposal) == f'Предложение от {item1} к {item2}'
    assert proposal.status == 'pending'

@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context

@pytest.mark.django_db
def test_my_items_requires_login(client):
    url = reverse('my_items')
    response = client.get(url)
    # В неавторизованном состоянии будет редирект на login
    assert response.status_code == 302
    assert '/login/' in response.url

@pytest.mark.django_db
def test_my_items_authenticated(client):
    user = User.objects.create_user(username='user')
    client.force_login(user)
    url = reverse('my_items')
    response = client.get(url)
    assert response.status_code == 200
    # Убедимся, что у пользователя нет еще объявлений
    assert len(response.context['items']) == 0

@pytest.mark.django_db
def test_create_item_form():
    from main.forms import ItemForm
    form_data = {
        'title': 'Form item',
        'description': 'desc',
        'category': 'книги',
        'condition': 'new'
    }
    form = ItemForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_exchangeproposal_form_save():
    from main.forms import ExchangeProposalForm
    user1 = User.objects.create_user(username='u1')
    user2 = User.objects.create_user(username='u2')
    item1 = Item.objects.create(user=user1, title='Item1', description='desc', category='книги', condition='new')
    item2 = Item.objects.create(user=user2, title='Item2', description='desc', category='мебель', condition='used')

    form_data = {
        'comment': 'Trade request',
    }
    form = ExchangeProposalForm(data=form_data, item_sender=item1, item_receiver=item2)
    assert form.is_valid()
    proposal = form.save()
    assert proposal.item_sender == item1
    assert proposal.item_receiver == item2
    assert proposal.comment == 'Trade request'
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CONDITIONS = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    item_sender = models.ForeignKey(Item, related_name='sent_proposals', on_delete=models.CASCADE)
    item_receiver = models.ForeignKey(Item, related_name='received_proposals', on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Предложение от {self.item_sender} к {self.item_receiver}'
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Item, ExchangeProposal
import json
import os

class Command(BaseCommand):
    help = 'Загружает тестовые данные пользователей, объявлений и предложений обмена из json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='exchange/main/sample_data.json',
            help='Путь к файлу с данными'
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f'Файл {path} не найден'))
            return

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        users_map = {}
        self.stdout.write('Создаем пользователей...')
        for user_info in data.get('users', []):
            user, created = User.objects.get_or_create(username=user_info['username'])
            if created:
                user.set_password(user_info['password'])
                user.save()
            users_map[user.username] = user

        self.stdout.write('Создаем объявления...')
        items_map = {}
        for item_info in data.get('items', []):
            user = users_map[item_info['user']]
            item, created = Item.objects.get_or_create(
                title=item_info['title'],
                user=user,
                defaults={
                    'description': item_info.get('description', ''),
                    'image_url': item_info.get('image_url', '') or None,
                    'category': item_info['category'],
                    'condition': item_info['condition'],
                }
            )
            items_map[item.title] = item

        self.stdout.write('Создаем предложения обмена...')
        for ex in data.get('exchange_proposals', []):
            sender_item = items_map[ex['item_sender_title']]
            receiver_item = items_map[ex['item_receiver_title']]
            ExchangeProposal.objects.get_or_create(
                item_sender=sender_item,
                item_receiver=receiver_item,
                defaults={
                    'comment': ex.get('comment', ''),
                    'status': ex['status']
                }
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))